from app.database.models import async_session
from app.database.models import Tariff


async def set_tariff(
        title: str, price: int, month_count: int
):
    async with async_session() as session:
        session.add(Tariff(title=title,
                           price=price,
                           month_count=month_count))
        await session.commit()