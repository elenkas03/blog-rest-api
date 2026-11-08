from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models, schemas
from fastapi import HTTPException

def create(db: Session, data: schemas.UserCreate) -> models.User:
    user = models.User(username=data.username, full_name=data.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get(db: Session, user_id: int) -> models.User:
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def list_(db: Session, username_contains: str | None = None, skip: int = 0, limit: int = 100):
    stmt = select(models.User)
    if username_contains:
        stmt = stmt.where(models.User.username.ilike(f"%{username_contains}%"))
    return db.execute(stmt.offset(skip).limit(limit)).scalars().all()

def update(db: Session, user_id: int, data: schemas.UserUpdate):
    user = get(db, user_id)
    if data.full_name is not None:
        user.full_name = data.full_name
    db.commit()
    db.refresh(user)
    return user

def delete(db: Session, user_id: int):
    user = get(db, user_id)
    db.delete(user)
    db.commit()
