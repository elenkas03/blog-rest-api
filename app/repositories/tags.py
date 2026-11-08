from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app import models, schemas

def create(db: Session, data: schemas.TagCreate) -> models.Tag:
    tag = models.Tag(name=data.name)
    db.add(tag); db.commit(); db.refresh(tag)
    return tag

def get(db: Session, tag_id: int) -> models.Tag:
    tag = db.get(models.Tag, tag_id)
    if not tag: raise HTTPException(404, "Tag not found")
    return tag

def list_(db: Session, skip=0, limit=100):
    return db.execute(select(models.Tag).offset(skip).limit(limit)).scalars().all()

def delete(db: Session, tag_id: int):
    tag = get(db, tag_id)
    db.delete(tag); db.commit()
