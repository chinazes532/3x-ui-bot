from app.database.models import async_session
from app.database.models import Subscription


async def set_subscription(
        tg_id: int,
        start_date: str,
        end_date: str,
        client_id: str
):
    async with async_session() as session:
        session.add(Subscription(tg_id=tg_id,
                                 start_date=start_date,
                                 end_date=end_date,
                                 client_id=client_id))
        await session.commit()