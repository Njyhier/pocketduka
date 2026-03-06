import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user_schemas import UserUpdate, UserWrite
from app.services.user.user_service import update_user, create_user, read_users
from pytest_asyncio