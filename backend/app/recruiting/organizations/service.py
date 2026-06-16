from sqlalchemy.ext.asyncio import AsyncSession

from app.recruiting.organizations.repository import OrganizationRepository
from app.recruiting.organizations.schema import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
)


class OrganizationService:
    def __init__(self, session: AsyncSession):
        self.repo = OrganizationRepository(session)
        self.session = session

    async def get(self, organization_id: int) -> OrganizationResponse | None:
        org = await self.repo.get_by_id(organization_id)
        if not org:
            return None

        return OrganizationResponse.model_validate(org)

    async def list(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> list[OrganizationResponse]:
        orgs = await self.repo.list(limit=limit, offset=offset)
        return [OrganizationResponse.model_validate(o) for o in orgs]

    async def create(self, data: OrganizationCreate) -> OrganizationResponse:
        # ビジネスルール例：名前重複チェック
        existing = await self.repo.search_by_name(data.name)
        if existing:
            # 完全一致だけ厳密チェック
            if any(o.name == data.name for o in existing):
                raise ValueError("Organization already exists")

        org = await self.repo.create(name=data.name)

        await self.session.commit()
        await self.session.refresh(org)

        return OrganizationResponse.model_validate(org)

    async def update(
        self,
        organization_id: int,
        data: OrganizationUpdate,
    ) -> OrganizationResponse | None:

        org = await self.repo.get_by_id(organization_id)
        if not org:
            return None

        if data.name is not None:
            org.name = data.name

        await self.session.commit()
        await self.session.refresh(org)

        return OrganizationResponse.model_validate(org)

    async def delete(self, organization_id: int) -> bool:
        result = await self.repo.delete(organization_id)

        if not result:
            return False

        await self.session.commit()
        return True