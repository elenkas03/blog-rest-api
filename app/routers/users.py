from fastapi import APIRouter, Depends, Query, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List
from app import schemas, models
from app.deps import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Създаване на потребител"
)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Създава нов потребител. Валидира уникалност на username.
    Връща 201 + създадения ресурс.
    """
    # Проверка за дублиран username (409 Conflict)
    exists = db.execute(
        select(func.count()).select_from(models.User).where(models.User.username == payload.username)
    ).scalar_one()
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    user = models.User(username=payload.username, full_name=payload.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get(
    "",
    response_model=List[schemas.UserRead],
    summary="Списък потребители с филтър"
)
def list_users(
    response: Response,
    username_contains: str | None = Query(
        None,
        description="Филтрира по част от потребителското име (case-insensitive)"),
    skip: int = Query(0, ge=0, description="Брой записи за прескачане (offset)"),
    limit: int = Query(100, ge=1, le=500, description="Максимален брой записи за връщане"),
    db: Session = Depends(get_db),
):
    """
    Връща списък от потребители, с опционален филтър по част от username,
    и пагинация чрез skip/limit. Добавя `X-Total-Count` за общия брой съвпадения.
    (Изискване: филтриране по част от потребителското име.)  # :contentReference[oaicite:2]{index=2}
    """
    stmt = select(models.User)
    count_stmt = select(func.count()).select_from(models.User)

    if username_contains:
        pattern = f"%{username_contains}%"
        stmt = stmt.where(models.User.username.ilike(pattern))
        count_stmt = count_stmt.where(models.User.username.ilike(pattern))

    total = db.execute(count_stmt).scalar_one()
    items = db.execute(stmt.offset(skip).limit(limit)).scalars().all()

    # Информираме клиента за общия брой съвпадения
    response.headers["X-Total-Count"] = str(total)
    return items

@router.get(
    "/{user_id}",
    response_model=schemas.UserRead,
    summary="Детайл за потребител"
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Връща един потребител по ID.
    Ако липсва — 404.
    """
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.patch(
    "/{user_id}",
    response_model=schemas.UserRead,
    summary="Частично обновяване на потребител"
)
def update_user(user_id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Частично обновяване (partial update) — засега поддържаме промяна на full_name.
    Ако липсва — 404.
    """
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if payload.full_name is not None:
        user.full_name = payload.full_name

    db.commit()
    db.refresh(user)
    return user

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Изтриване на потребител"
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Изтрива потребител по ID. Ако липсва — 404. Успех → 204 (без тяло).
    """
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
