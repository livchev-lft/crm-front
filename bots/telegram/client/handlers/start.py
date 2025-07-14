from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bots.telegram.async_requests.client_async_requests import client_check
from bots.telegram.client.kb import client_start_menu
from bots.telegram.client.kb import reg_num
from bots.telegram.client.fsm import ClientAuth
router = Router()

@router.message(Command("start"))
async def start_client(message: Message, state: FSMContext):
    check = await client_check(client_id=message.from_user.id)
    if check:
        await message.answer(text="зареган", reply_markup=client_start_menu)
    else:
        await state.set_state(ClientAuth.waiting_phone)
        await message.answer(
            text="Пожалуйста, отправьте свой номер телефона",
            reply_markup=reg_num
        )