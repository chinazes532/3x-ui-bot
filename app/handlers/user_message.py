import datetime

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.database.requests.admin.select import get_admins
from app.database.requests.tariff.select import get_tariff_by_id
from app.database.requests.user.add import set_user
from app.database.requests.user.select import get_user
from app.database.requests.subscription.select import get_subscription_by_tg_id

from app.utils.payments.ukassa import create_payment
from app.utils.payments.crypto_bot import create_crypto_payment
from app.utils.vpn_api.messages import get_connection_instructions

user = Router()


@user.callback_query(F.data == "check_sub")
async def check_sub(callback: CallbackQuery):
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    
    await callback.message.edit_text("Спасибо за подписку, вы можете пользоваться ботом!")

    await set_user(callback.from_user.id, callback.from_user.full_name, current_date)


@user.message(CommandStart())
async def start_command(message: Message):
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    await set_user(message.from_user.id, message.from_user.full_name, current_date)

    await message.answer("Добро пожаловать в бот для покупки VPN!",
                         reply_markup=ikb.user_panel)

    admins = await get_admins()

    for admin in admins:
        if admin.tg_id == message.from_user.id:
            await message.answer(f"Вы успешно авторизовались как администратор!",
                                 reply_markup=rkb.admin_menu)
            return


@user.callback_query(F.data == "tariffs_for_users")
async def tariffs_for_users(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Доступные тарифы:</b>",
        reply_markup=await bkb.users_tariffs_cb()
    )


@user.callback_query(F.data.startswith("usertariff_"))
async def check_user_tariff(callback: CallbackQuery):
    tariff_id = int(callback.data.split("_")[1])
    tariff = await get_tariff_by_id(tariff_id)

    await callback.message.edit_text(
        f"<b>{tariff.title}</b>\n"
        f"<b>Стоимость:</b> {tariff.price} руб.\n\n"
        f"<i>Выберите способ оплаты:</i>",
        reply_markup=await bkb.buy_tariff(tariff_id)
    )


@user.callback_query(F.data.startswith("pay_"))
async def pay(callback: CallbackQuery, bot: Bot):
    pay_method = callback.data.split("_")[1]
    tariff_id = int(callback.data.split("_")[2])

    if pay_method == "ru":
        await create_payment(callback, bot, tariff_id)
    elif pay_method == "crypto":
        await create_crypto_payment(tariff_id, callback.from_user.id, callback, bot)


@user.callback_query(F.data == "help")
async def help(callback: CallbackQuery):
    text = get_connection_instructions()

    await callback.message.edit_text(
        text=text,
        reply_markup=ikb.user_back,
        disable_web_page_preview=True
    )


@user.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    tg_id = callback.from_user.id
    user_info = await get_user(tg_id)
    subs = await get_subscription_by_tg_id(tg_id)
    is_sub = False

    text = f"""
    <b>Профиль пользователя</b>
    
<b>Имя пользователя:</b> {callback.from_user.full_name}
<b>Telegram ID:</b> <code>{user_info.tg_id}</code>
<b>Дата регистрации:</b> {user_info.date}
    """

    if subs:
        text += f"\n\n<b>Подписка активна до:</b> {subs.end_date}"
        is_sub = True

    await callback.message.edit_text(
        text=text,
        reply_markup=await bkb.profile_panel(is_sub)
    )


@user.callback_query(F.data == "extend_sub")
async def extend_sub(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>Выберите тариф для продления:</b>",
        reply_markup=await bkb.users_tariffs_cb()
    )


@user.callback_query(F.data == "user_back")
async def user_back(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Добро пожаловать в бот для покупки VPN!",
                         reply_markup=ikb.user_panel)

    await state.clear()

