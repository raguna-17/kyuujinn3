from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.recruiting.job_postings.model import JobPosting
from app.core.enums import EmploymentType


class JobPostingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # ===== 単体取得 =====
    async def get_by_id(self, job_id: int) -> JobPosting | None:
        result = await self.session.execute(
            select(JobPosting).where(JobPosting.id == job_id)
        )
        return result.scalar_one_or_none()

    # ===== 一覧取得（基本） =====
    async def list(
        self,
        limit: int = 5,
        offset: int = 0,
        only_active: bool = True,
    ) -> List[JobPosting]:

        stmt = select(JobPosting)

        if only_active:
            stmt = stmt.where(JobPosting.is_active == True)

        stmt = stmt.order_by(JobPosting.id.desc()).limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # ===== 会社別求人 =====
    async def list_by_organization(
        self,
        organization_id: int,
        limit: int = 50,
        offset: int = 0,
        only_active: bool = True,
    ) -> List[JobPosting]:

        stmt = select(JobPosting).where(
            JobPosting.organization_id == organization_id
        )

        if only_active:
            stmt = stmt.where(JobPosting.is_active == True)

        stmt = stmt.order_by(JobPosting.id.desc()).limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # ===== 作成 =====
    async def create(
        self,
        *,
        organization_id: int,
        user_id: int,
        description: str,
        salary: int,
        employment_type: EmploymentType,
    ) -> JobPosting:

        job = JobPosting(
            organization_id=organization_id,
            user_id=user_id,
            description=description,
            salary=salary,
            employment_type=employment_type,
        )

        self.session.add(job)
        await self.session.flush()
        return job

    # ===== 更新（部分更新） =====
    async def update(
        self,
        job_id: int,
        **kwargs,
    ) -> JobPosting | None:

        job = await self.get_by_id(job_id)
        if not job:
            return None

        for key, value in kwargs.items():
            if hasattr(job, key) and value is not None:
                setattr(job, key, value)

        return job

    # ===== 非公開化 =====
    async def deactivate(self, job_id: int) -> bool:
        job = await self.get_by_id(job_id)
        if not job:
            return False

        job.is_active = False
        return True

    # ===== 企業ID + ステータス更新系 =====
    async def close_job(self, job_id: int) -> bool:
        job = await self.get_by_id(job_id)
        if not job:
            return False

        job.is_active = False
        return True