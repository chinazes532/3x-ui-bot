from app.database.models import async_session
from app.database.models import Subscription
from sqlalchemy import delete


async def delete_subscription(tg_id: int):
    async with async_session() as session:
        await session.execute(
            delete(Subscription).where(Subscription.tg_id == tg_id)
        )
        await session.commit()