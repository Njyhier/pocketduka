from contextlib import asynccontextmanager
from app.db.db import create_db
from .routers import user_router, product_router, role_router
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(role_router.router)
