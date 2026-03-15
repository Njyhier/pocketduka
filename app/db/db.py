from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from dotenv import load_dotenv
import os
from app.models.Base import BaseModel

load_dotenv()
DB_URL = os.getenv("DB_URL")

engine: AsyncEngine = create_async_engine(DB_URL,echo=True)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
 