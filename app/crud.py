from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import random
from . import models, schemas

ANONYMOUS_NAMES = [
    "Anonymous Badger", "Secret Squirrel", "Hidden Hedgehog", "Incognito Iguana",
    "Masked Meerkat", "Private Penguin", "Covert Cobra", "Stealthy Salamander"
]

async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(models.Post).filter(models.Post.id == post_id)
    )
    return result.scalars().first()

async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Post).filter(models.Post.published == True).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_post(db: AsyncSession, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def update_post(db: AsyncSession, post_id: int, post_update: schemas.PostUpdate):
    db_post = await get_post(db, post_id)
    if not db_post:
        return None
    update_data = post_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def create_post_comment(db: AsyncSession, comment: schemas.CommentCreate, post_id: int):
    display_name = random.choice(ANONYMOUS_NAMES)
    db_comment = models.Comment(**comment.dict(), post_id=post_id, display_name=display_name)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment
