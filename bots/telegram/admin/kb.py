from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def new_app_admin(app_id: int, client_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="подтвердить заявку", callback_data=f"apply_app_{app_id}")],
            [InlineKeyboardButton(text="Отклонить", callback_data=f"reject_app_{app_id}")],
            [InlineKeyboardButton(text="👤 Открыть Telegram",url=f"tg://user?id={client_id}")]
        ]
    )

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Заявки")],
        [KeyboardButton(text="Добавить работника")],
    ],
    resize_keyboard=True
)

apps_filters = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="По статусу"), KeyboardButton(text="По номеру")],
        [KeyboardButton(text="По механику"), KeyboardButton(text="По клиенту")],
        [KeyboardButton(text="Сегодня"), KeyboardButton(text="Вчера"), KeyboardButton(text="За неделю")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)