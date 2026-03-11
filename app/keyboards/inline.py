from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import config

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Тарифы", callback_data="tariffs")],
        [InlineKeyboardButton(text="Рассылка", callback_data="sender")],
        [InlineKeyboardButton(text="Администраторы", callback_data="admins")],
    ]
)

admin_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
)

user_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Тарифы", callback_data="tariffs_for_users")],
        [InlineKeyboardButton(text="👤 Моя подписка", callback_data="profile")],
        [InlineKeyboardButton(text="🌟 Инструкции", callback_data="help")],
        [InlineKeyboardButton(text="👨‍💻 Поддержка", url="https://t.me/psych0ce00")],
    ]
)

user_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="user_back")]
    ]
)

check_sub = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", url=config.bot.channel_link)],
        [InlineKeyboardButton(text="Проверить подписку", callback_data="check_sub")]
    ]
)
