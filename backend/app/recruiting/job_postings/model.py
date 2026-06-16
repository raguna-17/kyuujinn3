from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func, Enum
from sqlalchemy.orm import relationship
from app.core.enums import EmploymentType
from app.db import Base


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    
    # 🔗 外部キー（超重要）
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False,index=True)

    description = Column(String(233), nullable=False)
    salary = Column(Integer, nullable=False)          
    employment_type = Column(Enum(EmploymentType), nullable=False) # 正社員 / インターンなど
    
    # 🔐 公開制御
    is_active = Column(Boolean, default=True, nullable=False)       # 公開/非公開
    closed_at = Column(DateTime, nullable=True)

    # ⏱ システム情報
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # 🔗 relations
    organization = relationship("Organization", back_populates="job_postings")
    user = relationship("User", back_populates="job_postings")  # ← ★追加
    applications = relationship(
        "JobApplication",
        back_populates="job_posting"
    )