from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.recruiting.job_applications.model import JobApplication
from app.core.enums import ApplicationStatus


class JobApplicationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # ===== 単体取得 =====
    async def get_by_id(self, application_id: int) -> JobApplication | None:
        result = await self.session.execute(
            select(JobApplication).where(JobApplication.id == application_id)
        )
        return result.scalar_one_or_none()

    # ===== ユーザー別一覧 =====
    async def list_by_user(
        self,
        user_id: int,
        limit: int = 5,
        offset: int = 0,
    ) -> list[JobApplication]:

        result = await self.session.execute(
            select(JobApplication)
            .where(JobApplication.user_id == user_id)
            .order_by(JobApplication.id.desc())
            .limit(limit)
            .offset(offset)
        )

        return list(result.scalars().all())

    # ===== 求人別一覧（企業側） =====
    async def list_by_job_posting(
        self,
        job_posting_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> list[JobApplication]:

        result = await self.session.execute(
            select(JobApplication)
            .where(JobApplication.job_posting_id == job_posting_id)
            .order_by(JobApplication.id.desc())
            .limit(limit)
            .offset(offset)
        )

        return list(result.scalars().all())

    # ===== 作成 =====
    async def create(
        self,
        *,
        user_id: int,
        job_posting_id: int,
        message: str | None = None,
        status: ApplicationStatus = ApplicationStatus.APPLIED,
    ) -> JobApplication:

        app = JobApplication(
            user_id=user_id,
            job_posting_id=job_posting_id,
            message=message,
            status=status,
        )

        self.session.add(app)
        await self.session.flush()

        return app

    # ===== 更新（柔軟更新） =====
    async def update(
        self,
        application_id: int,
        **kwargs,
    ) -> JobApplication | None:

        app = await self.get_by_id(application_id)
        if not app:
            return None

        for key, value in kwargs.items():
            if hasattr(app, key) and value is not None:
                setattr(app, key, value)

        return app

    # ===== ステータス更新専用 =====
    async def update_status(
        self,
        application_id: int,
        status: ApplicationStatus,
    ) -> JobApplication | None:

        app = await self.get_by_id(application_id)
        if not app:
            return None

        app.status = status
        return app

    # ===== 削除 =====
    async def delete(self, application_id: int) -> bool:
        app = await self.get_by_id(application_id)
        if not app:
            return False

        await self.session.delete(app)
        return True