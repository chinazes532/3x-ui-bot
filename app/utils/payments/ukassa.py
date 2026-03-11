import asyncio
import uuid
from datetime import datetime

from aiogram import Bot
from dateutil.relativedelta import relativedelta
from yookassa import Payment, Configuration
from aiogram.types import CallbackQuery

import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database.requests.admin.select import get_admins
from app.database.requests.subscription.update import update_subscription_end_date
from app.database.requests.tariff.select import get_tariff_by_id
from app.database.requests.subscription.select import get_subscription_by_tg_id
from app.database.requests.subscription.add import set_subscription

from app.utils.vpn_api.create_key import generate_key_for_user

from config import config



Configuration.account_id = config.ukassa.account_id
Configuration.secret_key = config.ukassa.secret_key


def create_invoice(tariff, user_id):
    return Payment.create({
        "amount": {
            "value": f"{tariff.price}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/TESTTEETTETTETETBOT"
        },
        "capture": True,
        # "save_payment_method": True,
        "description": f"{tariff.title}",
    }, uuid.uuid4())


async def create_payment(callback: CallbackQuery, bot: Bot, tariff_id):
    user_id = callback.from_user.id
    tariff = await get_tariff_by_id(tariff_id)
    user = await get_subscription_by_tg_id(user_id)
    payment = create_invoice(tariff, user_id)

    message = (
        f"<b>Вы выбрали тариф <u>{tariff.title}</u>\n\n"
        f"Сумма к оплате: {tariff.price} ₽</b>\n\n"
    ) if not user else (
        f"""<b>Вы выбрали тариф {tariff.title}
Для оплаты на сумму {tariff.price} ₽ нажмите на кнопку "Оплатить"
После оплаты подписка продлиться автоматически</b>"""
    )
    await callback.message.edit_text(message,
                                     reply_markup=await bkb.ukassa_pay(payment.confirmation.confirmation_url))

    asyncio.create_task(check_payment_status(payment.id, callback, bot, tariff_id))


async def check_payment_status(payment_id: str, callback: CallbackQuery, bot: Bot, tariff_id):
    timeout = 600  # Таймаут 10 минут (600 секунд), чтобы не ждать вечно
    elapsed = 0
    while elapsed < timeout:
        payment = Payment.find_one(payment_id)
        if payment.status == "succeeded":
            await finalize_payment(callback, bot, tariff_id)
            break
        await asyncio.sleep(3)
        elapsed += 3
    else:
        # Если таймаут истек, можно отправить сообщение пользователю
        # await callback.message.answer("Время ожидания оплаты истекло. Попробуйте снова.")
        pass


async def finalize_payment(callback: CallbackQuery, bot: Bot, tariff_id):
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
                     f'Способ оплаты: ЮKassa</b>',
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Ошибка при отправке сообщения админу {admin.tg_id}: {e}")






