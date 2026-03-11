from datetime import datetime

from app.database.models import async_session
from app.database.models import Subscription
from sqlalchemy import select, cast, DateTime


async def get_subscriptions():
    async with async_session() as session:
        subs = await session.scalars(select(Subscription))
        return subs


async def get_subscription_by_tg_id(tg_id: int):
    async with async_session() as session:
        sub = await session.scalar(select(Subscription).where(Subscription.tg_id == tg_id))
        return sub


async def get_expired_subscriptions():
    async with async_session() as session:
        result = await session.execute(
            select(Subscription).where(
                cast(Subscription.end_date, DateTime) <= datetime.now()
            )
        )
        return result.scalars().all()