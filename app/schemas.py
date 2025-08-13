from pydantic import BaseModel
from typing import List, Optional

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    display_name: str
    post_id: int
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: Optional[str] = None
    published: bool = False

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class Post(PostBase):
    id: int
    comments: List[Comment] = []
    class Config:
        from_attributes = True