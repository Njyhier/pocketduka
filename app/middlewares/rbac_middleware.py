from fastapi import HTTPException, status, Depends
from typing import Callable
from functools import wraps
from app.services.auth_service import get_current_user
import inspect
from app.models.user import User
from app.models.permissions import Permission
from app.services.permission_service import get_permission_by_name
from app.db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


async def require_role_permission(
    task: str,
    user: User,
    session: AsyncSession,
):
    print("RBAC  hit!")
    user = user
    # print(user)
    user_roles = [role.name for role in user.roles]
    # print("GETTING PERMISSION")
    permission: Permission = await get_permission_by_name(
        permission_name=task,
        session=session,
    )
    permission_roles = [role.name for role in permission.roles]
    # print("USER_ROLES", user_roles)
    # print("PERMISSION_ROLES", permission_roles)

    matching_roles = set(user_roles).intersection(permission_roles)
    if not matching_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
    print("Access granted!")
    return user


class SystemTasks:
    def __init__(self, task):
        self.task = task

    def __call__(self, fn: Callable):
        print("GETING CURRENT USER")
        user_dep = get_authorized_user(task_name=self.task)
        # print("USERDEP", user_dep)
        sig = inspect.signature(fn)
        params = list(sig.parameters.values())
        has_authorized_user = any(p.name == "authorized_user" for p in params)
        if not has_authorized_user:
            # print("No authorized user block is being used")
            new_param = inspect.Parameter(
                "authorized_user",
                inspect.Parameter.KEYWORD_ONLY,
                default=Depends(user_dep),
            )
            params.append(new_param)
            new_sig = sig.replace(parameters=params)
            # print("NEWSIGPARAM", new_param, new_sig)

            @wraps(fn)
            async def wrapper(*args, **kwargs):
                return await fn(
                    *args, **{k: v for k, v in kwargs.items() if k != "authorized_user"}
                )

            wrapper.__signature__ = new_sig
        else:

            @wraps(fn)
            async def wrapper(*args, **kwargs):
                return await fn(*args, **kwargs)

            wrapper.__signature__ = sig
        setattr(wrapper, "__task__", self.task)
        # print("WRAPPER", wrapper)
        return wrapper


def get_authorized_user(task_name: str):
    # print("Get authorized User Called")

    async def authorized_user(
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
    ):
        return await require_role_permission(
            task=task_name,
            user=user,
            session=session,
        )

    return authorized_user
