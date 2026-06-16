from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.recruiting.organizations.schema import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
)
from app.recruiting.organizations.service import OrganizationService
from app.dependencies import require_company_or_admin  # あなたの認可

router = APIRouter(prefix="/organizations", tags=["organizations"])


def get_service(db: AsyncSession = Depends(get_db)) -> OrganizationService:
    return OrganizationService(db)


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    data: OrganizationCreate,
    service: OrganizationService = Depends(get_service),
    _=Depends(require_company_or_admin),
):
    try:
        return await service.create(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
async def get_organization(
    organization_id: int,
    service: OrganizationService = Depends(get_service),
):
    org = await service.get(organization_id)

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    return org


@router.get(
    "",
    response_model=list[OrganizationResponse],
)
async def list_organizations(
    limit: int = 50,
    offset: int = 0,
    service: OrganizationService = Depends(get_service),
):
    return await service.list(limit=limit, offset=offset)


@router.patch(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
async def update_organization(
    organization_id: int,
    data: OrganizationUpdate,
    service: OrganizationService = Depends(get_service),
    _=Depends(require_company_or_admin),
):
    org = await service.update(organization_id, data)

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    return org


@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_organization(
    organization_id: int,
    service: OrganizationService = Depends(get_service),
    _=Depends(require_company_or_admin),
):
    ok = await service.delete(organization_id)

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    return None