from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from dotenv import load_dotenv
import os
from app.models.Base import BaseModel
from app.models import (
    address,
    category,
    product,
    inventory,
    permissions,
    user,
    roles,
    cart,
    cart_item,
)
from sqlalchemy import event


load_dotenv()
DB_URL = os.getenv("DB_URL")

engine: AsyncEngine = create_async_engine(DB_URL, echo=True)


@event.listens_for(engine.sync_engine, "connect")
def enable_sqlite_fk(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
