from app.database.models import async_session
from app.database.models import Tariff
from sqlalchemy import select


async def get_tariffs():
    async with async_session() as session:
        tariffs = await session.scalars(select(Tariff))
        return tariffs


async def get_tariff_by_id(id: int):
    async with async_session() as session:
        tariff = await session.scalar(select(Tariff).where(Tariff.id == id))
        return tariff