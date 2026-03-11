__all__ = ("cp")

import asyncio
from datetime import datetime

from aiogram import Bot
from aiogram.types import CallbackQuery
from aiosend import CryptoPay, TESTNET
from dateutil.relativedelta import relativedelta

from app.database.requests.admin.select import get_admins
from app.database.requests.subscription.add import set_subscription
from app.database.requests.subscription.select import get_subscription_by_tg_id
from app.database.requests.subscription.update import update_subscription_end_date
from app.utils.payments.parse_crypto import get_course_crypto
from app.utils.vpn_api.create_key import generate_key_for_user

from config import config

from app.database.requests.tariff.select import get_tariff_by_id

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

cp = CryptoPay(config.crypto_api.crypto_bot_token, TESTNET)


async def create_crypto_payment(
        tariff_id: int,
        tg_id: int,
        callback: CallbackQuery,
        bot: Bot
):
    tariff = await get_tariff_by_id(tariff_id)
    crypto_price = await get_course_crypto("tether")
    total_price = tariff.price / crypto_price

    invoice = await cp.create_invoice(total_price, "USDT")

    await callback.message.edit_text(
        f"<b>К оплате: <i>{total_price}</i> USDT\n"
        f"Оплатите счет, выставленный ниже 👇</b>",
        reply_markup=await bkb.crypto_pay(invoice.bot_invoice_url)
    )

    asyncio.create_task(check_crypto_status(invoice.invoice_id, callback, bot, tariff_id))


async def check_crypto_status(invoice_id: int, callback: CallbackQuery, bot: Bot, tariff_id):
    timeout = 600  # Таймаут 10 минут (600 секунд), чтобы не ждать вечно
    elapsed = 0
    while elapsed < timeout:
        invoice = await cp.get_invoice(invoice_id)
        if invoice.status == "paid":
            await finalize_crypto_payment(callback, bot, tariff_id)
            break
        await asyncio.sleep(3)
        elapsed += 3
    else:
        # Если таймаут истек, можно отправить сообщение пользователю
        # await callback.message.answer("Время ожидания оплаты истекло. Попробуйте снова.")
        pass


async def finalize_crypto_payment(callback: CallbackQuery, bot: Bot, tariff_id):
    user_id = callback.from_user.id
    user = await get_subscription_by_tg_id(user_id)
    tariff = await get_tariff_by_id(tariff_id)

    if not user:
        client_id = await generate_key_for_user(callback, user_id, callback.from_user.username)
        now = datetime.now()
        await set_subscription(user_id, str(now), str(now + relativedelta(months=tariff.month_count)), client_id)


    else:
        end = user.end_date if isinstance(user.end_date, datetime) else datetime.fromisoformat(user.end_date)
        new_end = end + relativedelta(days=tariff.month_count)
        await update_subscription_end_date(user_id, str(new_end))
        await callback.message.answer(
            f"<b>Ваша подписка была продлена до {new_end.strftime('%d.%m.%Y')}</b>",
            reply_markup=ikb.user_back
        )

    # Уведомление админов
    for admin in await get_admins():
        try:
            await bot.send_message(
                chat_id=admin.tg_id,
                text=f'<b>❗️Новая оплата❗️\n'
                     f'Пользователь <a href="tg://user?id={user_id}">{callback.from_user.full_name}</a>\n'
                     f'Название тарифа: {tariff.title}\n'
                     f'Стоимость: {tariff.price}₽\n'
                     f'Способ оплаты: CRYPTO</b>',
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Ошибка при отправке сообщения админу {admin.tg_id}: {e}")