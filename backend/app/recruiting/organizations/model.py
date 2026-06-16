from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.db import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)

    
    name = Column(String(233), nullable=False)              # 会社名
    
    # ⏱ システム情報
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at=Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)

    
    job_postings = relationship("JobPosting",back_populates="organization",cascade="all, delete-orphan")