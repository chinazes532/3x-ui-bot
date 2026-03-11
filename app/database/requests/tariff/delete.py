from app.database.models import async_session
from app.database.models import Tariff
from sqlalchemy import delete


async def delete_tariff_by_id(id: int):
    async with async_session() as session:
        await session.execute(
            delete(Tariff).where(Tariff.id == id)
        )
        await session.commit()