# Блог Платформа — REST API (FastAPI + SQLAlchemy + SQLite)

## Описание
REST API за блог платформа с единици: Потребители (Users), Публикации (Posts), Коментари (Comments) и Тагове (Tags).
Поддържа CRUD, релации 1:N и N:M, специфични ендпойнти и филтриране.

## Технологии
- FastAPI (уеб фреймуърк)
- SQLAlchemy 2.x (ORM)
- SQLite (база)
- Pydantic 2.x (валидация)

## Инсталация
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
