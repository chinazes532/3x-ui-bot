import os
import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as aioredis

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.utils.scheduler.check_sub import check_subscriptions

from app.filters.check_sub import CheckSubscription, CheckSubscriptionCallback
from app.filters.admin_filter import AdminProtect
from config import config

from app.handlers.user_message import user
from app.handlers.admin_message import admin
from app.handlers.tariff_message import tariff

from app.database.models import create_db

from app.utils.payments.crypto_bot import cp

scheduler = AsyncIOScheduler()


async def main():
    print("Bot is starting...")

    redis = await aioredis.from_url(config.redis.redis_url)
    await create_db()

    bot = Bot(token=config.bot.bot_token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=RedisStorage(redis))

    await create_db()

    # dp.message.middleware(CheckSubscription())
    # dp.callback_query.middleware(CheckSubscriptionCallback())

    admin.message.middleware(AdminProtect())
    admin.callback_query.middleware(AdminProtect())
    tariff.callback_query.middleware(AdminProtect())
    tariff.callback_query.middleware(AdminProtect())

    dp.include_router(user)
    dp.include_router(admin)
    dp.include_router(tariff)

    scheduler.add_job(check_subscriptions, 'interval', minutes=1, kwargs={'bot': bot})
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(cp.start_polling())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
