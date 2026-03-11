import uuid

from aiogram.types import CallbackQuery

from app.utils.vpn_api.messages import format_vless_config_message
from app.utils.vpn_api.xui_api import xui_api


async def generate_key_for_user(
        callback: CallbackQuery,
        tg_id: int, username: str = "username"
):
    random_uuid = uuid.uuid4()
    email = f"tg_id_{tg_id}_{username}_{random_uuid}"
    client = xui_api.create_client(
        inbound_id=1,
        email=email,
        total_gb=0,  # Безлимит (используем настройки 3x-ui по умолчанию)
        expiry_time=0,  # Бессрочно
        enable=True,
    )

    if not client:
        await callback.message.answer("❌ Ошибка создания ключа")
        return

    vless_url = xui_api.get_client_config(1, email)

    inbound = xui_api.get_inbound(1)
    inbound_name = inbound.remark if inbound else f"Inbound {1}"

    try:
        # Форматируем сообщение используя централизованный шаблон
        user_message = format_vless_config_message(
            vless_url=vless_url,
            title="✅ <b>Ваш ключ готов!</b>",
        )

        # Отправляем ключ пользователю
        await callback.message.answer(user_message)

        return client.id

    except Exception as e:
        await callback.message.answer(
            f"⚠️ Ключ создан, но не удалось отправить пользователю {str(e)}"
        )