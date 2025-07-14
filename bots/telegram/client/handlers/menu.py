from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bots.telegram.async_requests.client_async_requests import check_client_car, check_apps, check_cars, check_car_app
from bots.telegram.client.fsm import EditCar, CreateApp
from bots.telegram.client.handlers.app import process_chosen_car
from bots.telegram.client.kb import choose_car, get_delete_car_keyboard, client_add_car, client_edit_car

router = Router()

@router.message(F.text=="🚗 Мои автомобили")
async def my_cars(message: Message, state: FSMContext):
    client_id = message.from_user.id
    cars = await check_cars(client_id)
    if cars:
        await state.set_state(EditCar.check)
        await message.answer("Ваши машины:", reply_markup=client_edit_car)
        for car in cars:
            text = (
                f"🚗 <b>Машина</b>\n"
                f"<b>Марка:</b> {car['brand']}\n"
                f"<b>Модель:</b> {car['model']}\n"
                f"<b>Номер:</b> {car['number']}\n"
                f"<b>Год:</b> {car['year']}"
            )
            keyboard = get_delete_car_keyboard(car['id'])
            await message.answer(text, parse_mode="HTML", reply_markup=keyboard)
    else:
        await message.answer("У вас пока нет машин, хотите добавить?", reply_markup=client_add_car)

@router.message(F.text=="➕ Новая заявка")
async def create_app(message: Message, state: FSMContext):
    client_id = message.from_user.id
    cars = await check_cars(client_id)
    apps = await check_apps(client_id)
    if len(cars) == 1:
        if apps:
            await message.answer(f"У вас уже есть созданная заявка!\n"
                                 f"\n"
                                 f"Если хотите то вы можете удалить заявку или добавить другую машину\n")
            return
        await process_chosen_car(message, cars[0], state)
    elif len(cars) > 1:
        await state.set_state(CreateApp.choose_car)
        await message.answer("Выберите машину")
        for car in cars:
            result = await check_car_app(car['id'])
            if result:
                text = (
                    f"Заявка уже есть‼️‼️‼️\n"
                    f"🚗 <b>Машина</b>\n"
                    f"<b>Марка:</b> {car['brand']}\n"
                    f"<b>Модель:</b> {car['model']}\n"
                    f"<b>Номер:</b> {car['number']}\n"
                    f"<b>Год:</b> {car['year']}"
                )
                await message.answer(text, parse_mode="HTML")
            else:
                text = (
                    f"🚗 <b>Машина</b>\n"
                    f"<b>Марка:</b> {car['brand']}\n"
                    f"<b>Модель:</b> {car['model']}\n"
                    f"<b>Номер:</b> {car['number']}\n"
                    f"<b>Год:</b> {car['year']}"
                )
                keyboard = choose_car(car['id'])
                await message.answer(text, parse_mode="HTML", reply_markup=keyboard)
    else:
        await message.answer("У вас пока нет добавленных машин", reply_markup=client_add_car)


@router.message(F.text=="📋 Мои заявки")
async def my_apps(message: Message, state: FSMContext):
    client_id = message.from_user.id
    apps = await check_apps(client_id)
    if apps:
        for app in apps:
            car = await check_client_car(app['car_id'])
            text = (
                f"Заявка N{app['id']}\n"
                f"\n"
                f"🚗 Машина:\n"
                f"Марка: {car['brand']}\n"
                f"Модель: {car['model']}\n"
                f"Номер: {car['number']}\n"
                f"Год: {car['year']}\n"
                f"\n"
                f"📋 Проблема:\n"
                f"{app['problem']}\n"
                f"📞 Контакт\n"
            )
            await message.answer(text, parse_mode="HTML")
    if not apps:
        await message.answer("Заявок нет")
    else:
        await message.answer("ошибка")
