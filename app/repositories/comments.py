from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app import models, schemas

def create_for_post(db: Session, post_id: int, data: schemas.CommentCreate) -> models.Comment:
    post = db.get(models.Post, post_id)
    if not post: raise HTTPException(404, "Post not found")
    user = db.get(models.User, data.user_id)
    if not user: raise HTTPException(404, "User not found")
    c = models.Comment(content=data.content, user_id=data.user_id, post_id=post_id)
    db.add(c); db.commit(); db.refresh(c)
    return c

def get(db: Session, comment_id: int) -> models.Comment:
    c = db.get(models.Comment, comment_id)
    if not c: raise HTTPException(404, "Comment not found")
    return c

def list_for_post(db: Session, post_id: int, skip=0, limit=100):
    return db.execute(
        select(models.Comment).where(models.Comment.post_id == post_id).offset(skip).limit(limit)
    ).scalars().all()

def delete(db: Session, comment_id: int):
    c = get(db, comment_id)
    db.delete(c); db.commit()
