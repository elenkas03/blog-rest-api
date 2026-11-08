from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.deps import get_db
from app.repositories import tags as repo

router = APIRouter(prefix="/tags", tags=["tags"])

@router.post(
    "",
    response_model=schemas.TagRead,
    status_code=status.HTTP_201_CREATED,
    summary="Създаване на таг"
)
def create_tag(payload: schemas.TagCreate, db: Session = Depends(get_db)):
    """Създава нов таг (уникално име)."""
    return repo.create(db, payload)

@router.get(
    "",
    response_model=List[schemas.TagRead],
    summary="Списък с тагове"
)
def list_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Връща списък с тагове (с пагинация)."""
    return repo.list_(db, skip, limit)

@router.delete(
    "/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Изтриване на таг"
)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """Изтрива таг по ID. Успех → 204 No Content."""
    repo.delete(db, tag_id)
