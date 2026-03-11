from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests.admin.select import get_admins
from app.database.requests.tariff.select import get_tariffs


async def admins_cb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить администратора", callback_data="add_admin"))

    admins = await get_admins()
    for admin in admins:
        kb.row(InlineKeyboardButton(text=f"{admin.tg_id}", callback_data=f"admin_{admin.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def edit_admin(id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"deleteadmin_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"admins"))

    return kb.as_markup()


async def tariffs_cb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="➕ Добавить тариф", callback_data="add_tariff"))

    tariffs = await get_tariffs()
    for tariff in tariffs:
        kb.row(InlineKeyboardButton(text=f"{tariff.title}", callback_data=f"tariff_{tariff.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))

    return kb.as_markup()


async def edit_tariff(id: int):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="✏️ Изменить название", callback_data=f"edit_tariff_title_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить стоимость", callback_data=f"edit_tariff_price_{id}"))
    kb.row(InlineKeyboardButton(text="✏️ Изменить кол-во мес.", callback_data=f"edit_tariff_month_count_{id}"))
    kb.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_tariff_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="tariffs"))

    return kb.as_markup()


async def users_tariffs_cb():
    kb = InlineKeyboardBuilder()

    tariffs = await get_tariffs()
    for tariff in tariffs:
        kb.row(InlineKeyboardButton(text=f"{tariff.title}", callback_data=f"usertariff_{tariff.id}"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="user_back"))

    return kb.as_markup()


async def buy_tariff(id: int):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="🇷🇺 РФ Карты", callback_data=f"pay_ru_{id}"))
    kb.row(InlineKeyboardButton(text="🪙 Криптовалюта", callback_data=f"pay_crypto_{id}"))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="tariffs_for_users"))

    return kb.as_markup()


async def ukassa_pay(url):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="💰 Оплатить", url=url))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="tariffs_for_users"))

    return kb.as_markup()


async def crypto_pay(url):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="💰 Оплатить", url=url))
    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="tariffs_for_users"))

    return kb.as_markup()


async def profile_panel(is_sub: bool):
    kb = InlineKeyboardBuilder()

    if is_sub:
        kb.row(InlineKeyboardButton(text="Продлить подписку", callback_data="extend_sub"))

    kb.row(InlineKeyboardButton(text="🔙 Назад", callback_data="user_back"))

    return kb.as_markup()