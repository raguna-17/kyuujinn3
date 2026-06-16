from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db

from app.users.schema import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
)

from app.users.service import (
    create_user,
    authenticate_user,
)

from app.dependencies import get_current_active_user
from app.users.model import User


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):

    user = await create_user(user_data, db)

    return user


@router.post("/login", response_model= TokenResponse,)
async def login_user(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):

    tokens = await authenticate_user(user_data, db)

    return tokens


@router.get(
    "/me",
    response_model=UserResponse,
)
async def read_me(
    current_user: User = Depends(get_current_active_user),
):

    return current_user