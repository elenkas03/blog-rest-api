# Blog Platform — REST API

A REST API for a blog platform built with **FastAPI**, **SQLAlchemy 2** and **SQLite**. It models users, posts, comments and tags, including one-to-many and many-to-many relations, filtering and pagination.

Coursework for *Web Server Programming* — Plovdiv University "Paisii Hilendarski". (Bulgarian version: [README_BG.md](README_BG.md))

## Tech stack

- FastAPI — web framework with automatic OpenAPI docs
- SQLAlchemy 2.x — ORM
- SQLite — database (`blog.db` is created on first run)
- Pydantic 2.x — request / response validation
- Uvicorn — ASGI server

## Data model

```
User 1 ──── N Post  N ──── N Tag      (post_tags association table)
User 1 ──── N Comment N ──── 1 Post
```

Deleting a user or a post cascades to the related posts / comments.

## Endpoints

| Resource | Endpoints |
|---|---|
| Users | `POST /users`, `GET /users`, `GET /users/{id}`, `PATCH /users/{id}`, `DELETE /users/{id}` |
| Posts | `POST /posts`, `GET /posts`, `GET /posts/{id}`, `PATCH /posts/{id}`, `DELETE /posts/{id}`, `GET /posts/by-user/{user_id}`, `POST /posts/{post_id}/tags/{tag_id}` |
| Comments | `GET /comments/for-post/{post_id}`, `POST /comments/for-post/{post_id}`, `GET /comments/{id}`, `DELETE /comments/{id}` |
| Tags | `POST /tags`, `GET /tags`, `DELETE /tags/{id}` |
| Health | `GET /health` |

- `GET /posts` supports filtering by tag name (`?tag=...`) and pagination (`skip`, `limit`).
- `GET /posts/by-user/{user_id}` supports `skip` and `limit`.

## Project structure

```
app/
├── main.py          Application setup, router registration, /health
├── database.py      Engine and session
├── models.py        SQLAlchemy models
├── schemas.py       Pydantic schemas
├── deps.py          Dependencies (DB session)
├── repositories/    Data access layer (users, posts, comments, tags)
└── routers/         HTTP layer (users, posts, comments, tags)
```

The code is split into routers (HTTP), repositories (queries) and schemas (validation).

## Running locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

## Author

Elenka Spasova Gishina — Faculty of Mathematics and Informatics, Plovdiv University.
