from contextlib import asynccontextmanager
from app.db.db import create_db
from .routes import user_router
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router.router)
