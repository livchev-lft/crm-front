from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

reg_num = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

client_start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚗 Мои автомобили")],
        [KeyboardButton(text="➕ Новая заявка"), KeyboardButton(text="📋 Мои заявки")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

client_add_car = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🚗 Добавить автомобиль", callback_data="add_car")],
]
)

client_edit_car = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚗 Добавить автомобиль"), KeyboardButton(text="⬅️ Назад")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

def get_delete_car_keyboard(car_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Удалить машину", callback_data=f"delete_car:{car_id}")]
        ]
    )

def choose_car(car_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Выбрать", callback_data=f"choose_car:{car_id}")]
        ]
    )
menu_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="В меню")],
    ],
    resize_keyboard=True
)

repair_choice = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔧 Диагностика"), KeyboardButton(text="⚙️ Замена масла")],
        [KeyboardButton(text="🛞 Подвеска"), KeyboardButton(text="🧯 Тормоза")],
        [KeyboardButton(text="💡 Электрика"), KeyboardButton(text="🧊 Кондиционер")],
        [KeyboardButton(text="🔋 Аккумулятор"), KeyboardButton(text="🔩 Двигатель")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

tg_or_phone = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Telegram")],
        [KeyboardButton(text="📞По телефону")],
    ],
    resize_keyboard=True
)

yes_no_phone = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data = "yes_phone"),
         InlineKeyboardButton(text="Нет", callback_data = "no_phone")]
    ]
)