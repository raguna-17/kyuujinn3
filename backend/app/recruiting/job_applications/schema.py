from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import ApplicationStatus


# ===== 共通ベース =====
class JobApplicationBase(BaseModel):
    message: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


# ===== 作成 =====
class JobApplicationCreate(JobApplicationBase):
    job_posting_id: int


# ===== 更新 =====
class JobApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None


# ===== レスポンス =====
class JobApplicationResponse(JobApplicationBase):
    id: int

    user_id: int
    job_posting_id: int
    message: Optional[str]
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)