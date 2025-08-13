import json
from fastapi import Depends, FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from . import crud, models, schemas
from .database import engine, get_db
from .dependencies import get_current_user
from .websocket import manager, broadcaster

app = FastAPI(
    title="Real-Time Comments API",
    description="A configurable FastAPI backend with PostgreSQL and WebSockets.",
    version="1.1.0"
)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    await broadcaster.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await broadcaster.disconnect()

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/posts/", response_model=List[schemas.Post])
async def read_posts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    posts = await crud.get_posts(db, skip=skip, limit=limit)
    return posts

@app.get("/posts/{post_id}", response_model=schemas.Post)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    db_post = await crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.post("/posts/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: schemas.PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return await crud.create_post(db=db, post=post)

@app.put("/posts/{post_id}", response_model=schemas.Post)
async def update_post(
    post_id: int,
    post_update: schemas.PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_post = await crud.update_post(db=db, post_id=post_id, post_update=post_update)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.post("/posts/{post_id}/comments/", response_model=schemas.Comment, status_code=status.HTTP_201_CREATED)
async def create_comment_for_post(
    post_id: int, comment: schemas.CommentCreate, db: AsyncSession = Depends(get_db)
):
    db_post = await crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    new_comment = await crud.create_post_comment(db=db, comment=comment, post_id=post_id)
    
    comment_data = schemas.Comment.from_orm(new_comment).dict()
    await manager.broadcast_to_post(post_id, json.dumps(comment_data))
    
    return new_comment

@app.websocket("/ws/posts/{post_id}")
async def websocket_endpoint(websocket: WebSocket, post_id: int):
    await manager.connect(websocket, post_id)
    channel = f"post_{post_id}"
    try:
        async with broadcaster.subscribe(channel=channel) as subscriber:
            async for event in subscriber:
                await websocket.send_text(event.message)
    except WebSocketDisconnect:
        manager.disconnect(websocket, post_id)
        print(f"Client disconnected from post {post_id}")