from aiogram import Bot

from app.database.requests.subscription.delete import delete_subscription
from app.database.requests.subscription.select import get_expired_subscriptions
from app.utils.vpn_api.xui_api import xui_api


async def send_message_middleware(bot: Bot, tg_id: int):
    try:
        await delete_subscription(tg_id)
        await bot.send_message(tg_id,
                               f"<b>Ваша подписка закончилась!</b>\n\n",)

    except Exception as e:
        await delete_subscription(tg_id)


async def check_subscriptions(bot: Bot):
    expired_users = await get_expired_subscriptions()
    for subscription in expired_users:
        tg_id = subscription.tg_id
        xui_api.delete_client(1, subscription.client_id)
        await send_message_middleware(bot=bot, tg_id=tg_id)