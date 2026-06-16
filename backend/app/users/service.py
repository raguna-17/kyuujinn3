from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from app.users.model import User
from app.users.schema import (
    UserCreate,
    UserLogin,
)

from app.core.enums import (
    UserRole,
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)


async def create_user(
    user_data: UserCreate,
    db: AsyncSession,
) -> User:

    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=user_data.email,

        hashed_password=hash_password(
            user_data.password
        ),

        # RegisterRole → UserRoleへ変換
        role=UserRole(user_data.role.value),
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user


async def authenticate_user(
    user_data: UserLogin,
    db: AsyncSession,
) -> dict:

    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(
        user_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),

            # Enumはvalueで入れる
            "role": user.role.value,
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": str(user.id),
            "role": user.role.value,
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role,
    }


async def get_user_by_id(
    user_id: int,
    db: AsyncSession,
) -> User | None:

    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    return result.scalar_one_or_none()