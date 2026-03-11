from app.database.models import async_session
from app.database.models import Tariff
from sqlalchemy import update


async def update_tariff_title(id: int, title: str):
    async with async_session() as session:
        await session.execute(
            update(Tariff).where(Tariff.id == id).values(title=title)
        )
        await session.commit()


async def update_tariff_price(id: int, price: int):
    async with async_session() as session:
        await session.execute(
            update(Tariff).where(Tariff.id == id).values(price=price)
        )
        await session.commit()


async def update_tariff_month_count(id: int, month_count: int):
    async with async_session() as session:
        await session.execute(
            update(Tariff).where(Tariff.id == id).values(month_count=month_count)
        )
        await session.commit()