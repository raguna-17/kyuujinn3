from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.recruiting.organizations.model import Organization


class OrganizationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # 取得（単体）
    async def get_by_id(self, organization_id: int) -> Organization | None:
        result = await self.session.execute(
            select(Organization).where(Organization.id == organization_id)
        )
        return result.scalar_one_or_none()

    # 一覧取得
    async def list(self, limit: int = 50, offset: int = 0) -> list[Organization]:
        result = await self.session.execute(
            select(Organization)
            .order_by(Organization.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    # 作成
    async def create(self, name: str) -> Organization:
        org = Organization(name=name)
        self.session.add(org)
        await self.session.flush()  # id取得したい時用
        return org

    # 更新
    async def update_name(self, organization_id: int, name: str) -> Organization | None:
        org = await self.get_by_id(organization_id)
        if not org:
            return None

        org.name = name
        return org

    # 削除
    async def delete(self, organization_id: int) -> bool:
        org = await self.get_by_id(organization_id)
        if not org:
            return False

        await self.session.delete(org)
        return True

    # 名前検索（最低限の実用機能）
    async def search_by_name(self, keyword: str, limit: int = 20) -> List[Organization]:
        result = await self.session.execute(
            select(Organization)
            .where(Organization.name.ilike(f"%{keyword}%"))
            .limit(limit)
        )
        return list(result.scalars().all())