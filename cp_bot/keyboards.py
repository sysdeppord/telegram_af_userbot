from pyrogram.types import InlineKeyboardButton
"""FUCKING BOT KEYBOARDS"""
select_existing = [
    [InlineKeyboardButton("🆕 Создать автоматически", callback_data="destination_create_new")],
    [InlineKeyboardButton("⚙️ В меню настроек", callback_data="setting")],
    [InlineKeyboardButton("🏠 В главное меню", callback_data="main_menu")]
]
start_message = [
    [InlineKeyboardButton("📶 Статус", callback_data="status")],
    [InlineKeyboardButton("⚙️ Настройки", callback_data="setting")],
    [InlineKeyboardButton("ℹ️ О боте", callback_data="about")]
]
auth_ok = [
    [InlineKeyboardButton("🏠 В главное меню", callback_data="main_menu")]
]
add = [
    [InlineKeyboardButton("👤 Отправлю контакт пользователя", callback_data="add_from_send_contact_step1")],
    [InlineKeyboardButton("👉💬 Выберу чат с пользователем", callback_data="add_from_exist_chat_step1")],
    [InlineKeyboardButton("👉👤 Выберу из списка контактов", callback_data="add_from_sync_contact_step1")],
    [InlineKeyboardButton("🔃💬 Перешлю его сообщение", callback_data="add_from_forwarded_message_step1")],
    [InlineKeyboardButton("🔃📰 Добавить в пересылку канал", callback_data="add_to_forward_channel")],
    [InlineKeyboardButton("🔃👥 Добавить в пересылку группу", callback_data="add_to_forward_group")],
    [InlineKeyboardButton("⚙️ Назад в меню настроек", callback_data="setting")],
    [InlineKeyboardButton("🏠 Назад в главное меню", callback_data="main_menu")]
]
setting = [
    [InlineKeyboardButton("🏃‍♂️ Запустить бота", callback_data="start")],
    [InlineKeyboardButton("⛔️ Остановить бота", callback_data="stop")],
    [InlineKeyboardButton("📝 Список пересылки", callback_data="list")],
    [InlineKeyboardButton("🥶 Заморозить пересылку от", callback_data="freeze_step1")],
    [InlineKeyboardButton("❌🥶 Разморозить пересылку от", callback_data="unfreeze_step1")],
    [InlineKeyboardButton("➕ Добавить в пересылку", callback_data="add")],
    [InlineKeyboardButton("➖ Удалить с пересылки", callback_data="remove_step1")],
    [InlineKeyboardButton("🔁 Пересылать свои сообщения", callback_data="forward_my_step1")],
    [InlineKeyboardButton("🔀 Изменить канал для пересылки", callback_data="change_destination_step1")],
    [InlineKeyboardButton("🔥 Сжечь всё!", callback_data="burn_all")],
    [InlineKeyboardButton("❌ Удалить свой аккаунт", callback_data="wipe_me")],
    [InlineKeyboardButton("🔰 Помощь по боту", callback_data="help")],
    [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
    [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
]
wipe_me = [
    [InlineKeyboardButton("ДА, УДАЛИТЬ МОЙ АККАУНТ", callback_data="wipe_me_yes")],
    [InlineKeyboardButton("НЕТ, Я ХОЧУ НАЗАД К МАМОЧКЕ", callback_data="wipe_me_no")]
]
add_select_destination = [
    [InlineKeyboardButton("🆕 Создать автоматически", callback_data="destination_create_new")],
    [InlineKeyboardButton("➕ Выбрать существующий", callback_data="destination_select_existing_step1")],
    [InlineKeyboardButton("⚙️ В меню настроек", callback_data="setting")],
    [InlineKeyboardButton("🏠 В главное меню", callback_data="main_menu")]
]
enter_code = [
    [InlineKeyboardButton("1️⃣", callback_data="code_1"),
    InlineKeyboardButton("2️⃣", callback_data="code_2"),
    InlineKeyboardButton("3️⃣", callback_data="code_3")],
    [InlineKeyboardButton("4️⃣", callback_data="code_4"),
    InlineKeyboardButton("5️⃣", callback_data="code_5"),
    InlineKeyboardButton("6️⃣", callback_data="code_6")],
    [InlineKeyboardButton("7️⃣", callback_data="code_7"),
    InlineKeyboardButton("8️⃣", callback_data="code_8"),
    InlineKeyboardButton("9️⃣", callback_data="code_9")],
    [InlineKeyboardButton("🆗", callback_data="code_ok"),
    InlineKeyboardButton("0️⃣", callback_data="code_0"),
    InlineKeyboardButton("↩️", callback_data="code_remove")]
]
bottom_button = [
    [InlineKeyboardButton("⚙️ Назад в меню настроек", callback_data="setting")],
    [InlineKeyboardButton("🏠 Назад в главное меню", callback_data="main_menu")]
]
after_add = [
    [InlineKeyboardButton("➕ Добавить ещё", callback_data="add")],
    [InlineKeyboardButton("⚙️ Назад в меню настроек", callback_data="setting")],
    [InlineKeyboardButton("🏠 Назад в главное меню", callback_data="main_menu")]
]
burn_all = [
    [InlineKeyboardButton("ДА! СЖЕЧЬ ВСЁ К ХУЯМ", callback_data="fbi_open_up")],
    [InlineKeyboardButton("НЕТ! ХОЧУ НАЗАД К МАМОЧКЕ!", callback_data="main_menu")]
]
forward_my_off = [
    [InlineKeyboardButton("🆕 ОТЛЮЧИТЬ", callback_data="forward_my_off")],
    [InlineKeyboardButton("⚙️ В меню настроек", callback_data="setting")],
    [InlineKeyboardButton("🏠 В главное меню", callback_data="main_menu")]
]
forward_my_on = [
    [InlineKeyboardButton("🆕 ВКЛЮЧИТЬ", callback_data="forward_my_on")],
    [InlineKeyboardButton("⚙️ В меню настроек", callback_data="setting")],
    [InlineKeyboardButton("🏠 В главное меню", callback_data="main_menu")]
]
nav_list = [
    [InlineKeyboardButton("Далее ⏩", callback_data="in_list_next")],
    [InlineKeyboardButton("⏪ Назад", callback_data="in_list_previous")]
]
