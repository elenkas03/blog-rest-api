from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# -------- Tag --------
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagRead(TagBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# -------- User --------
class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    full_name: Optional[str] = None

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# -------- Comment --------
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    user_id: int  # авторът на коментара

class CommentRead(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    post_id: int

# -------- Post --------
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    user_id: int

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostRead(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    tags: List[TagRead] = []
