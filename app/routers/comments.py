from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.deps import get_db
from app.repositories import comments as repo

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get(
    "/for-post/{post_id}",
    response_model=List[schemas.CommentRead],
    summary="Коментари за публикация"
)
def list_comments_for_post(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Връща всички коментари към конкретна публикация (с пагинация)."""
    return repo.list_for_post(db, post_id, skip, limit)

@router.post(
    "/for-post/{post_id}",
    response_model=schemas.CommentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Създаване на коментар към публикация"
)
def create_comment_for_post(post_id: int, payload: schemas.CommentCreate, db: Session = Depends(get_db)):
    """Създава нов коментар към посочената публикация от конкретен потребител."""
    return repo.create_for_post(db, post_id, payload)

@router.get(
    "/{comment_id}",
    response_model=schemas.CommentRead,
    summary="Детайл за коментар"
)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """Връща коментар по ID, 404 ако липсва."""
    return repo.get(db, comment_id)

@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Изтриване на коментар"
)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """Изтрива коментар по ID. Успех → 204 No Content."""
    repo.delete(db, comment_id)
