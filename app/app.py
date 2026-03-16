from contextlib import asynccontextmanager
from app.db.db import create_db
from .routers import (
    user_router,
    product_router,
    role_router,
    permission_router,
    image_router,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods="*",
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(role_router.router)
app.include_router(permission_router.router)
app.include_router(image_router.router)
