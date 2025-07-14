from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bots.telegram.async_requests.client_async_requests import reg_client_request
from bots.telegram.client.handlers.start import ClientAuth
from bots.telegram.client.kb import client_start_menu

router = Router()

@router.message(ClientAuth.waiting_phone, F.contact)
async def add_phone(message: Message, state: FSMContext):
    await state.clear()
    contact = message.contact
    client_id = message.from_user.id
    user_name = message.from_user.username
    phone = contact.phone_number

    client_data = {
        "client_id": client_id,
        "user_name": user_name,
        "phone": phone
    }
    response = await reg_client_request(client_data)
    if response:
        await message.answer("Вы успешно зарегистрированы!")
        await message.answer("Меню", reply_markup=client_start_menu)
    else:
        await message.answer("Ошибка регистрации. Попробуйте позже.")
