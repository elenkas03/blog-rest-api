from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users, posts, comments, tags

#Създава таблиците при първо стартиране
Base.metadata.create_all(bind=engine)

# създава приложението
app = FastAPI(title="Blog Platform REST API")

#добавяме маршрути
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(tags.router)

#добавяме health check
@app.get("/health")
def health():
    return {"status": "ok"}
