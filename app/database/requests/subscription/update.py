from app.database.models import async_session
from app.database.models import Subscription
from sqlalchemy import update


async def update_subscription_end_date(tg_id: int, end_date: str):
    async with async_session() as session:
        await session.execute(
            update(Subscription).where(Subscription.tg_id == tg_id).values(end_date=end_date)
        )
        await session.commit()