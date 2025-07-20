from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

sup_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Регистрация сотрудника")],
        [KeyboardButton(text="Удаление сотрудника")],
        [KeyboardButton(text="Статистика")],
        [KeyboardButton(text="Заявки")],
    ]
)