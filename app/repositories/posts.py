from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app import models, schemas

def create(db: Session, data: schemas.PostCreate) -> models.Post:
    user = db.get(models.User, data.user_id)
    if not user: raise HTTPException(404, "User not found")
    post = models.Post(title=data.title, content=data.content, user_id=data.user_id)
    db.add(post); db.commit(); db.refresh(post)
    return post

def get(db: Session, post_id: int) -> models.Post:
    post = db.get(models.Post, post_id)
    if not post: raise HTTPException(404, "Post not found")
    return post

def list_(db: Session, tag: str | None = None, skip: int = 0, limit: int = 100):
    if tag:
        stmt = (
            select(models.Post)
            .join(models.post_tags)
            .join(models.Tag)
            .where(models.Tag.name == tag)
        )
    else:
        stmt = select(models.Post)
    return db.execute(stmt.offset(skip).limit(limit)).scalars().all()

def update(db: Session, post_id: int, data: schemas.PostUpdate):
    post = get(db, post_id)
    if data.title is not None: post.title = data.title
    if data.content is not None: post.content = data.content
    db.commit(); db.refresh(post)
    return post

def delete(db: Session, post_id: int):
    post = get(db, post_id)
    db.delete(post); db.commit()

def list_by_user(db: Session, user_id: int, skip=0, limit=100):
    return db.execute(
        select(models.Post).where(models.Post.user_id == user_id).offset(skip).limit(limit)
    ).scalars().all()

def add_tag(db: Session, post_id: int, tag_id: int) -> models.Post:
    post = get(db, post_id)
    tag = db.get(models.Tag, tag_id)
    if not tag: raise HTTPException(404, "Tag not found")
    if tag not in post.tags:
        post.tags.append(tag)
        db.commit(); db.refresh(post)
    return post
