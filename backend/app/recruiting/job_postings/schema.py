from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.core.enums import EmploymentType


# ===== 共通 =====
class JobPostingBase(BaseModel):
    description: str = Field(
        min_length=1,
        max_length=233,
    )

    salary: int = Field(
        ge=0,
        le=999999,
    )

    employment_type: EmploymentType

    is_active: bool = True

    closed_at: Optional[datetime] = None


# ===== 作成 =====
class JobPostingCreate(JobPostingBase):
    organization_id: int


# ===== 更新 =====
class JobPostingUpdate(BaseModel):
    description: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=233,
    )

    salary: Optional[int] = Field(
        default=None,
        ge=0,
        le=999999,
    )

    employment_type: Optional[EmploymentType] = None

    is_active: Optional[bool] = None

    closed_at: Optional[datetime] = None


# ===== レスポンス =====
class JobPostingResponse(JobPostingBase):
    id: int

    user_id: int
    organization_id: int

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)