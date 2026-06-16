from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.recruiting.job_postings.repository import JobPostingRepository
from app.recruiting.job_postings.schema import (
    JobPostingCreate,
    JobPostingUpdate,
    JobPostingResponse,
)


class JobPostingService:
    def __init__(self, session: AsyncSession):
        self.repo = JobPostingRepository(session)
        self.session = session

    # ===== 単体取得 =====
    async def get(self, job_id: int) -> JobPostingResponse | None:
        job = await self.repo.get_by_id(job_id)
        if not job:
            return None

        return JobPostingResponse.model_validate(job)

    # ===== 一覧（公開用） =====
    async def list(
        self,
        limit: int = 5,
        offset: int = 0,
    ) -> List[JobPostingResponse]:

        jobs = await self.repo.list(limit=limit, offset=offset)

        return [
            JobPostingResponse.model_validate(j)
            for j in jobs
        ]

    # ===== 会社別一覧 =====
    async def list_by_organization(
        self,
        organization_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> List[JobPostingResponse]:

        jobs = await self.repo.list_by_organization(
            organization_id=organization_id,
            limit=limit,
            offset=offset,
        )

        return [
            JobPostingResponse.model_validate(j)
            for j in jobs
        ]

    # ===== 作成 =====
    async def create(
        self,
        data: JobPostingCreate,
        user_id: int,
    ) -> JobPostingResponse:

        # ビジネスルール①：最低限のチェック（例）
        if data.salary < 0:
            raise ValueError("salary is invalid")

        job = await self.repo.create(
            organization_id=data.organization_id,
            user_id=user_id,
            description=data.description,
            salary=data.salary,
            employment_type=data.employment_type,
        )

        await self.session.commit()
        await self.session.refresh(job)

        return JobPostingResponse.model_validate(job)

    # ===== 更新 =====
    async def update(
        self,
        job_id: int,
        data: JobPostingUpdate,
    ) -> JobPostingResponse | None:

        job = await self.repo.get_by_id(job_id)
        if not job:
            return None

        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            return JobPostingResponse.model_validate(job)

        # ビジネスルール②：閉鎖済み求人は更新不可
        if job.closed_at is not None:
            raise ValueError("closed job cannot be updated")

        updated_job = await self.repo.update(
            job_id,
            **update_data,
        )

        await self.session.commit()
        await self.session.refresh(updated_job)

        return JobPostingResponse.model_validate(updated_job)

    # ===== 非公開化 =====
    async def deactivate(self, job_id: int) -> bool:

        job = await self.repo.get_by_id(job_id)
        if not job:
            return False

        await self.repo.deactivate(job_id)

        await self.session.commit()
        return True

    # ===== 募集終了 =====
    async def close(self, job_id: int) -> bool:

        job = await self.repo.get_by_id(job_id)
        if not job:
            return False

        if job.closed_at is None:
            from datetime import datetime
            job.closed_at = datetime.utcnow()

        job.is_active = False

        await self.session.commit()
        return True