from pydantic import BaseModel,ConfigDict, Field
from typing import Optional
from datetime import datetime


# ===== 共通ベース =====
class OrganizationBase(BaseModel):
    name: str= Field(min_length=1, max_length=233)


# ===== 作成 =====
class OrganizationCreate(OrganizationBase):
    pass


# ===== 更新 =====
class OrganizationUpdate(BaseModel):
    name: Optional[str] = None


# ===== レスポンス =====
class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)