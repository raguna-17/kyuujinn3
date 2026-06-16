from pydantic import BaseModel, EmailStr, ConfigDict, Field
from app.core.enums import UserRole, RegisterRole

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=4, max_length=128)
    role: RegisterRole= RegisterRole.USER

class UserLogin(UserBase):
    password: str = Field(min_length=4, max_length=128)

class UserResponse(UserBase):
    id: int
    is_active: bool
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    role: str