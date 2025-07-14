import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

from bots.telegram.async_requests.client_async_requests import delete_car_request, add_car_request
from bots.telegram.client.kb import menu_button, client_start_menu
from bots.telegram.client.handlers.menu import EditCar
from bots.telegram.client.fsm import AddCar
router = Router()

@router.callback_query(F.data == "add_car")
async def add_car_callback(call: CallbackQuery, state: FSMContext):
    client_id = call.from_user.id
    await state.update_data(client_id=client_id)
    await state.set_state(AddCar.brand)
    await call.message.answer("Введите бренд автомобиля", reply_markup=menu_button)

@router.message(F.text=="🚗 Добавить автомобиль")
async def add_car_message(message: Message, state: FSMContext):
    client_id = message.from_user.id
    await state.update_data(client_id=client_id)
    await state.set_state(AddCar.brand)
    await message.answer("Введите бренд автомобиля", reply_markup=menu_button)

@router.message(AddCar.brand)
async def add_car_model(message: Message, state: FSMContext):
    if message.text == "В меню":
        await go_menu(message, state)
        return
    brand = message.text
    await state.update_data(brand=brand)
    await state.set_state(AddCar.model)
    await message.answer("Введите модель машины")

@router.message(AddCar.model)
async def add_car_number(message: Message, state: FSMContext):
    if message.text == "В меню":
        await go_menu(message, state)
        return
    model = message.text
    await state.update_data(model=model)
    await state.set_state(AddCar.number)
    await message.answer("Введите номер машины")

@router.message(AddCar.number)
async def add_car_year(message: Message, state: FSMContext):
    if message.text == "В меню":
        await go_menu(message, state)
        return
    number = message.text.strip()
    if not re.fullmatch(r"[А-ЯA-Z]{1,2}\d{3}[А-ЯA-Z]{2}\d{2,3}", number):
        await message.answer("❌ Неверный формат номера. Пример: А123ВС77")
        return
    await state.update_data(number=number)
    await state.set_state(AddCar.year)
    await message.answer("Введите год машины")

@router.message(AddCar.year)
async def add_car_finish(message: Message, state: FSMContext):
    if message.text == "В меню":
        await go_menu(message, state)
        return
    year_text = message.text.strip()
    if not year_text.isdigit():
        await message.answer("❌ Год должен быть числом, например: 2015")
        return

    year = int(year_text)
    if year < 1900 or year > 2100:
        await message.answer("❌ Неверный год. Введите значение от 1900 до 2100.")
        return
    await state.update_data(year=year)
    data = await state.get_data()

    await message.answer(
        f"Добавляем машину:\n"
        f"Бренд: {data['brand']}\n"
        f"Модель: {data['model']}\n"
        f"Номер: {data['number']}\n"
        f"Год: {data['year']}"
    )
    await state.clear()
    add_car = await add_car_request(data)
    if add_car:
        await message.answer("Машина успешно добавлена")
        await message.answer("Меню", reply_markup=client_start_menu)
    else:
        await message.answer("Ошибка добавления машины")

@router.message(EditCar.check, F.text == "⬅️ Назад")
async def back_from_cars(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Меню", reply_markup=client_start_menu)

@router.callback_query(EditCar.check, F.data.startswith("delete_car:"))
async def delete_car_callback(call: CallbackQuery, state: FSMContext):
    car_id = int(call.data.split(":")[1])
    await state.clear()
    response = await delete_car_request(car_id)
    if response:
        await call.message.answer("Машина успешно удалена.")
        await call.message.answer("Меню", reply_markup=client_start_menu)
    else:
        await call.message.answer("ошибка")

@router.message(StateFilter("*"), F.text=="В меню")
async def go_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Меню", reply_markup=client_start_menu)