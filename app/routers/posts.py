from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.deps import get_db
from app.repositories import posts as repo

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post(
    "",
    response_model=schemas.PostRead,
    status_code=status.HTTP_201_CREATED,
    summary="Създаване на публикация"
)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    """Създава нов пост (публикация) за съществуващ потребител."""
    return repo.create(db, payload)

@router.get(
    "",
    response_model=List[schemas.PostRead],
    summary="Списък с публикации (по избор филтър по таг)"
)
def list_posts(
    tag: str | None = Query(None, description="Филтър по име на таг"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """Връща публикации. Ако е подаден `tag`, филтрира по име на таг."""
    return repo.list_(db, tag, skip, limit)

@router.get(
    "/{post_id}",
    response_model=schemas.PostRead,
    summary="Детайл за публикация"
)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Връща публикация по ID, 404 ако липсва."""
    return repo.get(db, post_id)

@router.patch(
    "/{post_id}",
    response_model=schemas.PostRead,
    summary="Частично обновяване на публикация"
)
def update_post(post_id: int, payload: schemas.PostUpdate, db: Session = Depends(get_db)):
    """Обновява заглавие/съдържание. Връща обновения пост."""
    return repo.update(db, post_id, payload)

@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Изтриване на публикация"
)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Изтрива публикация по ID. Успех → 204 No Content."""
    repo.delete(db, post_id)

# Специфичен ендпойнт: всички постове на конкретен потребител
@router.get(
    "/by-user/{user_id}",
    response_model=List[schemas.PostRead],
    summary="Всички публикации на потребител"
)
def posts_by_user(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Връща постове, създадени от посочения потребител."""
    return repo.list_by_user(db, user_id, skip, limit)

# Специфичен ендпойнт: асоцииране на съществуващ таг към пост
@router.post(
    "/{post_id}/tags/{tag_id}",
    response_model=schemas.PostRead,
    summary="Добавяне на таг към публикация"
)
def add_tag_to_post(post_id: int, tag_id: int, db: Session = Depends(get_db)):
    """Асoциира вече съществуващ таг с дадена публикация."""
    return repo.add_tag(db, post_id, tag_id)
