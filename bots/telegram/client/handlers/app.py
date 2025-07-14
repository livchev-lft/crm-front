import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bots.telegram.async_requests.client_async_requests import replace_phone_request, client_check, check_cars, post_app_request
from bots.telegram.client.handlers.menu import CreateApp
from bots.telegram.client.kb import repair_choice, tg_or_phone, yes_no_phone, client_start_menu
from bots.telegram.admin.handlers.app import send_for_admin
router = Router()

@router.callback_query(CreateApp.choose_car, F.data.startswith("choose_car:"))
async def handle_car_choice(call: CallbackQuery, state: FSMContext):
    car_id = int(call.data.split(":")[1])
    client_id = call.from_user.id
    cars = await check_cars(client_id)
    car = next((c for c in cars if c["id"] == car_id), None)
    if car:
        await call.answer()
        await process_chosen_car(call.message, car, state)
    else:
        await call.answer("Машина не найдена", show_alert=True)

async def process_chosen_car(message: Message, car: dict, state: FSMContext):
    await state.update_data(car_id=car['id'])
    await state.set_state(CreateApp.start)
    await message.answer(
        f"<b>Выбрана машина:</b>\n"
        f"<b>Марка:</b> {car['brand']}\n"
        f"<b>Модель:</b> {car['model']}\n"
        f"<b>Номер:</b> {car['number']}\n"
        f"<b>Год:</b> {car['year']}",
        parse_mode="HTML"
    )
    await message.answer("Опишите проблему или выберите из предложенных ниже", reply_markup=repair_choice)

@router.message(CreateApp.start)
async def conn_apply(message: Message, state: FSMContext):
    await state.update_data(client_id=message.from_user.id)
    await state.update_data(problem=message.text)
    await message.answer("Для уточнения деталей наш администратор свяжется с вами, выберете как хотите связаться", reply_markup=tg_or_phone)
    await state.set_state(CreateApp.connect_apply)

@router.message(CreateApp.connect_apply, F.text == "Telegram")
async def apply_tg(message: Message, state: FSMContext):
    await state.update_data(conn = 0)
    data = await state.get_data()
    response = await post_app_request(data)
    if response:
        await message.answer("Спасибо за оставленную заявку, администратор свяжется с вами как можно скорее")
        await send_for_admin(response["id"], message)
        await message.answer("Меню", reply_markup=client_start_menu)
        await state.clear()
    else:
        await message.answer("ошибка добавления заявки")
        await state.clear()
        await message.answer("Меню", reply_markup=client_start_menu)

@router.message(CreateApp.connect_apply, F.text == "📞По телефону")
async def apply_number(message: Message, state: FSMContext):
    await state.update_data(conn = 1)
    await state.set_state(CreateApp.phone_apply)
    check = await client_check(client_id=message.from_user.id)
    await message.answer(f"Это ваш номер телефона?\n"
                         f"{check['phone']}\n", reply_markup=yes_no_phone)

@router.callback_query(CreateApp.phone_apply, F.data == "yes_phone")
async def yes_phone(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    response = await post_app_request(data)
    if response:
        await call.message.answer("Спасибо за оставленную заявку, администратор свяжется с вами как можно скорее")
        await send_for_admin(response["id"], call.message)
        await call.message.answer("Меню", reply_markup=client_start_menu)
        await state.clear()
    else:
        await call.message.answer("ошибка добавления заявки")
        await state.clear()
        await call.message.answer("Меню", reply_markup=client_start_menu)

@router.callback_query(CreateApp.phone_apply, F.data == "no_phone")
async def edit_phone(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите свой номер телефона в формате +79999999999")
    await state.set_state(CreateApp.edit_phone)

@router.message(CreateApp.edit_phone)
async def post_edit_phone_and_app(message: Message, state: FSMContext):
    phone_regex = r"^\+7\d{10}$"
    phone = message.text.strip()
    if not re.match(phone_regex, phone):
        await message.answer("❌ Неверный формат номера. Введите в формате +79991234567")
        return
    await state.update_data(phone=phone)
    await state.update_data(conn = 1)
    await replace_phone_request(client_id = message.from_user.id, phone = phone)
    data = await state.get_data()
    response = await post_app_request(data)
    if response:
        await message.answer("✅ Номер сохранён. Заявка отправлена!")
        await message.answer("Спасибо за оставленную заявку, администратор свяжется с вами как можно скорее")
        await send_for_admin(response["id"], message)
        await state.clear()
        await message.answer("Меню", reply_markup=client_start_menu)
    else:
        await message.answer("ошибка добавления заявки")
        await state.clear()
        await message.answer("Меню", reply_markup=client_start_menu)

