def format_bytes(size: int) -> str:
    """Форматирует байты в читаемый вид (KB, MB, GB, TB)."""
    power = 2**10
    magnitude = 0
    prefixes = ("", "K", "M", "G", "T")
    while size >= power and magnitude + 1 < len(prefixes):
        size /= power
        magnitude += 1
    return f"{size:.2f} {prefixes[magnitude]}B"


def format_vless_config_message(
    vless_url: str | None,
    title: str = "✅ Ваш ключ готов!",
) -> str:
    """
    Форматирование сообщения с VLESS конфигом и предупреждением о приватности

    Args:
        email: Email клиента
        inbound_name: Название/remark inbound
        vless_url: URL VLESS конфигурации
        title: Заголовок сообщения

    Returns:
        Отформатированный текст сообщения
    """
    message = f"{title}\n\n"

    if vless_url:
        message += (
            f"🔗 <b>VLESS конфиг:</b>\n"
            f"<pre><code class='language-text'>{vless_url}</code></pre>\n\n"
            f"{get_privacy_warning()}"
        )
    else:
        message += "⚠️ Не удалось получить конфигурацию"

    return message


def get_connection_instructions() -> str:
    """
    Получить стандартные инструкции по подключению для VPN клиентов
    """
    return (
        "📱 <b>Рекомендуемые приложения:</b>\n"
        "• <b>Hiddify</b> (Все платформы 🌍): <a href='https://hiddify.com/#app'>Сайт</a> | <a href='https://github.com/hiddify/hiddify-app'>GitHub</a>\n"  # noqa: E501
        "• <b>v2rayTun</b> (Все платформы 🌍): <a href='https://v2raytun.com/'>Сайт</a> | <a href='https://apps.apple.com/en/app/v2raytun/id6476628951'>App Store</a> | <a href='https://play.google.com/store/apps/details?id=com.v2raytun.android'>Play Store</a>\n"  # noqa: E501
        "• <b>NekoBox</b> (Android 🤖 / Windows 💻): <a href='https://getnekobox.com/en/'>Сайт</a> | <a href='https://github.com/MatsuriDayo/NekoBoxForAndroid'>GitHub</a>\n"  # noqa: E501
        "• <b>FoXray</b> (Android 🤖 / iOS 🍎 / macOS 🍏): <a href='https://foxray.org/'>Сайт</a> | <a href='https://play.google.com/store/apps/details?id=com.github.foxray'>Play Store</a> | <a href='https://apps.apple.com/ru/app/v2raytun/id6476628951'>App Store</a>\n"  # noqa: E501
        "• <b>v2rayN</b> (Windows 💻): <a href='https://en.v2rayn.org/'>Сайт</a> | <a href='https://github.com/2dust/v2rayN'>GitHub</a>\n"  # noqa: E501
        "• <b>v2rayNG</b> (Android 🤖): <a href='https://en.v2rayng.org'>Сайт</a> | <a href='https://github.com/2dust/v2rayNG'>GitHub</a> | <a href='https://play.google.com/store/apps/details?id=com.v2ray.ang'>Play Store</a>\n\n"  # noqa: E501
        "🚀 <b>Как подключиться:</b>\n"
        "1. Скопируйте <code>vless://</code> ссылку выше\n"
        "2. Откройте приложение и нажмите ➕ (или «Импорт из буфера»)\n"
        "3. Нажмите на добавленный профиль для подключения"
    )


def get_privacy_warning() -> str:
    """
    Получить предупреждение о приватности VPN конфига

    Returns:
        Отформатированный текст предупреждения
    """
    return "⚠️ <b>Это приватный VPN!</b> Не передавайте ключ посторонним."


def get_feedback_reminder() -> str:
    """
    Получить напоминание об обратной связи (связь с админом)

    Returns:
        Отформатированный текст напоминания
    """
    return "💬 Есть вопрос? Просто напиши его в этот чат — админ ответит."


def get_loading_inbounds_msg() -> str:
    """Сообщение о загрузке списка inbound'ов"""
    return "⏳ <b>Загрузка списка inbound'ов...</b>\n\nПожалуйста, подождите."


def get_creating_key_msg() -> str:
    """Сообщение о создании ключа"""
    return "⏳ Создаю ключ..."


def get_cloning_inbound_msg(remark: str) -> str:
    """Сообщение о клонировании inbound"""
    return f"⏳ Клонирую inbound '{remark}' и создаю ключ..."


def get_error_creating_key_msg() -> str:
    """Сообщение об ошибке создания ключа"""
    return (
        "❌ <b>Ошибка создания ключа</b>\n\n" "Проверьте логи 3x-ui или попробуйте другой inbound."
    )


def get_loading_clients_msg() -> str:
    """Сообщение о загрузке списка клиентов"""
    return "⏳ <b>Загрузка списка клиентов...</b>\n\nПожалуйста, подождите."


def get_loading_stats_msg() -> str:
    """Сообщение о загрузке статистики"""
    return "⏳ <b>Загрузка статистики...</b>\n\nПожалуйста, подождите."


def format_key_info_message(
    email: str,
    comment: str,
    inbound_remark: str,
    status: str,
    traffic_info: str,
    expiry_info: str,
    vless_url: str | None,
) -> str:
    """
    Форматирование детального сообщения с информацией о ключе и предупреждением

    Args:
        email: Email клиента
        comment: Комментарий к ключу
        inbound_remark: Название inbound
        status: Текст статуса (например, "✅ Активен")
        traffic_info: Информация о лимите трафика
        expiry_info: Информация о сроке действия
        vless_url: URL VLESS конфигурации

    Returns:
        Отформатированный текст сообщения
    """
    message = (
        f"🔑 <b><code>{email}</code></b>\n\n"
        f"📝 Комментарий: {comment}\n"
        f"🖥 Inbound: {inbound_remark}\n"
        f"{status}\n"
        f"{traffic_info}\n"
        f"{expiry_info}\n\n"
    )

    if vless_url:
        message += (
            f"🔗 <b>VLESS конфиг:</b>\n"
            f"<pre><code class='language-text'>{vless_url}</code></pre>\n\n"
            f"{get_privacy_warning()}"
        )
    else:
        message += "⚠️ Не удалось получить конфигурацию"

    return message