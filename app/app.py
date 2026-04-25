from contextlib import asynccontextmanager
from app.db.db import create_db
from .routers import (
    user_router,
    product_router,
    role_router,
    permission_router,
    image_router,
    inventory_router,
    category_router,
    address_router,
    cart_item_router,
    cart_router,
    order_router,
    payments_router,
)

from app.routers.users import users_routes
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pocketduka.vercel.app",
        "http://localhost:4200",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods="*",
    allow_headers=["*"],
)

app.include_router(users_routes.router)
app.include_router(product_router.router)
app.include_router(role_router.router)
app.include_router(permission_router.router)
app.include_router(image_router.router)
app.include_router(inventory_router.router)
app.include_router(category_router.router)
app.include_router(address_router.router)
app.include_router(cart_router.router)
app.include_router(cart_item_router.router)
app.include_router(order_router.router)
app.include_router(payments_router.router)
