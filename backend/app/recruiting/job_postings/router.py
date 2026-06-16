from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.recruiting.job_postings.schema import (
    JobPostingCreate,
    JobPostingUpdate,
    JobPostingResponse,
)
from app.recruiting.job_postings.service import JobPostingService

from app.dependencies import require_company_or_admin, get_current_active_user


router = APIRouter(prefix="/job-postings", tags=["job-postings"])


def get_service(db: AsyncSession = Depends(get_db)) -> JobPostingService:
    return JobPostingService(db)


# ===== 作成 =====
@router.post(
    "",
    response_model=JobPostingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_job_posting(
    data: JobPostingCreate,
    service: JobPostingService = Depends(get_service),
    user=Depends(get_current_active_user),
    _=Depends(require_company_or_admin),
):
    try:
        return await service.create(data, user_id=user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ===== 単体取得 =====
@router.get(
    "/{job_id}",
    response_model=JobPostingResponse,
)
async def get_job_posting(
    job_id: int,
    service: JobPostingService = Depends(get_service),
):
    job = await service.get(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found",
        )

    return job


# ===== 一覧（公開用） =====
@router.get(
    "",
    response_model=list[JobPostingResponse],
)
async def list_job_postings(
    limit: int = 5,
    offset: int = 0,
    service: JobPostingService = Depends(get_service),
):
    return await service.list(limit=limit, offset=offset)


# ===== 会社別一覧 =====
@router.get(
    "/organization/{organization_id}",
    response_model=list[JobPostingResponse],
)
async def list_by_organization(
    organization_id: int,
    limit: int = 50,
    offset: int = 0,
    service: JobPostingService = Depends(get_service),
    _=Depends(require_company_or_admin),
):
    return await service.list_by_organization(
        organization_id=organization_id,
        limit=limit,
        offset=offset,
    )


# ===== 更新 =====
@router.patch(
    "/{job_id}",
    response_model=JobPostingResponse,
)
async def update_job_posting(
    job_id: int,
    data: JobPostingUpdate,
    service: JobPostingService = Depends(get_service),
    _=Depends(require_company_or_admin),
):
    try:
        job = await service.update(job_id, data)

        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job posting not found",
            )

        return job

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ===== 非公開化 =====
@router.patch(
    "/{job_id}/deactivate",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def deactivate_job_posting(
    job_id: int,
    service: JobPostingService = Depends(get_service),
    _=Depends(require_company_or_admin),
):
    ok = await service.deactivate(job_id)

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found",
        )

    return None


# ===== 募集終了 =====
@router.patch(
    "/{job_id}/close",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def close_job_posting(
    job_id: int,
    service: JobPostingService = Depends(get_service),
    _=Depends(require_company_or_admin),
):
    ok = await service.close(job_id)

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found",
        )

    return None