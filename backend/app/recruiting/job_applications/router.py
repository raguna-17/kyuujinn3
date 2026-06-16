from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.recruiting.job_applications.schema import (
    JobApplicationCreate,
    JobApplicationUpdate,
    JobApplicationResponse,
)
from app.recruiting.job_applications.service import JobApplicationService

from app.dependencies import (
    get_current_active_user,
    require_user_or_admin,
    require_company_or_admin,
)

router = APIRouter(prefix="/job-applications", tags=["job-applications"])


# ===== DI =====
def get_service(db: AsyncSession = Depends(get_db)) -> JobApplicationService:
    return JobApplicationService(db)


# =========================================================
# 応募作成（USER or ADMIN）
# =========================================================
@router.post(
    "",
    response_model=JobApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_application(
    data: JobApplicationCreate,
    service: JobApplicationService = Depends(get_service),
    user=Depends(require_user_or_admin),
):
    try:
        return await service.create(data, user_id=user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =========================================================
# 自分の応募一覧（USER or ADMIN）
# =========================================================
@router.get(
    "/me",
    response_model=list[JobApplicationResponse],
)
async def list_my_applications(
    limit: int = 50,
    offset: int = 0,
    service: JobApplicationService = Depends(get_service),
    user=Depends(require_user_or_admin),
):
    return await service.list_my_applications(
        user_id=user.id,
        limit=limit,
        offset=offset,
    )


# =========================================================
# 応募詳細（USER or ADMIN）
# =========================================================
@router.get(
    "/{application_id}",
    response_model=JobApplicationResponse,
)
async def get_application(
    application_id: int,
    service: JobApplicationService = Depends(get_service),
    user=Depends(require_user_or_admin),
):
    app = await service.get(application_id)

    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return app


# =========================================================
# 応募削除（USER or ADMIN）
# =========================================================
@router.delete(
    "/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_application(
    application_id: int,
    service: JobApplicationService = Depends(get_service),
    user=Depends(require_user_or_admin),
):
    ok = await service.delete(application_id)

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return None


# =========================================================
# 企業：求人ごとの応募一覧（COMPANY or ADMIN）
# =========================================================
@router.get(
    "/job/{job_posting_id}",
    response_model=list[JobApplicationResponse],
)
async def list_by_job_posting(
    job_posting_id: int,
    limit: int = 50,
    offset: int = 0,
    service: JobApplicationService = Depends(get_service),
    _=Depends(require_company_or_admin),
):
    return await service.list_by_job_posting(
        job_posting_id=job_posting_id,
        limit=limit,
        offset=offset,
    )


# =========================================================
# 企業：ステータス更新（COMPANY or ADMIN）
# =========================================================
@router.patch(
    "/{application_id}/status",
    response_model=JobApplicationResponse,
)
async def update_status(
    application_id: int,
    data: JobApplicationUpdate,
    service: JobApplicationService = Depends(get_service),
    _=Depends(require_company_or_admin),
):
    if data.status is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="status is required",
        )

    try:
        app = await service.update_status(
            application_id,
            status=data.status,
        )

        if not app:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        return app

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )