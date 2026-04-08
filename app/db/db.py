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
if not DB_URL:
    raise ValueError("DATABASE_URL is not set")

engine: AsyncEngine = create_async_engine(DB_URL, echo=True)


@event.listens_for(engine.sync_engine, "connect")
def enable_sqlite_fk(dbapi_connection, connection_record):
    from sqlite3 import Connection as SQLite3Connection

    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        print(BaseModel.metadata.tables.keys())
