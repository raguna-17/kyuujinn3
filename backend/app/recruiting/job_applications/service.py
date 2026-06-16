from sqlalchemy.ext.asyncio import AsyncSession

from app.recruiting.job_applications.repository import JobApplicationRepository
from app.recruiting.job_applications.schema import (
    JobApplicationCreate,
    JobApplicationUpdate,
    JobApplicationResponse,
)
from app.core.enums import ApplicationStatus


class JobApplicationService:
    def __init__(self, session: AsyncSession):
        self.repo = JobApplicationRepository(session)
        self.session = session

    # ===== 応募作成（ユーザー） =====
    async def create(
        self,
        data: JobApplicationCreate,
        user_id: int,
    ) -> JobApplicationResponse:

        app = await self.repo.create(
            user_id=user_id,
            job_posting_id=data.job_posting_id,
            message=data.message,
        )

        await self.session.commit()
        await self.session.refresh(app)

        return JobApplicationResponse.model_validate(app)

    # ===== ユーザー: 自分の応募一覧 =====
    async def list_my_applications(
        self,
        user_id: int,
        limit: int = 5,
        offset: int = 0,
    ) -> list[JobApplicationResponse]:

        apps = await self.repo.list_by_user(
            user_id=user_id,
            limit=limit,
            offset=offset,
        )

        return [
            JobApplicationResponse.model_validate(a)
            for a in apps
        ]

    # ===== 企業: 求人ごとの応募一覧 =====
    async def list_by_job_posting(
        self,
        job_posting_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> list[JobApplicationResponse]:

        apps = await self.repo.list_by_job_posting(
            job_posting_id=job_posting_id,
            limit=limit,
            offset=offset,
        )

        return [
            JobApplicationResponse.model_validate(a)
            for a in apps
        ]

    # ===== ステータス更新（企業側） =====
    async def update_status(
        self,
        application_id: int,
        status: ApplicationStatus,
    ) -> JobApplicationResponse | None:

        app = await self.repo.get_by_id(application_id)
        if not app:
            return None

        # 軽い状態制御（最低限）
        if app.status == ApplicationStatus.REJECTED:
            raise ValueError("Cannot update rejected application")

        updated = await self.repo.update_status(application_id, status)

        await self.session.commit()
        await self.session.refresh(updated)

        return JobApplicationResponse.model_validate(updated)

    # ===== 応募詳細 =====
    async def get(
        self,
        application_id: int,
    ) -> JobApplicationResponse | None:

        app = await self.repo.get_by_id(application_id)
        if not app:
            return None

        return JobApplicationResponse.model_validate(app)

    # ===== 削除（基本はユーザー or 管理者） =====
    async def delete(self, application_id: int) -> bool:

        ok = await self.repo.delete(application_id)

        if not ok:
            return False

        await self.session.commit()
        return True