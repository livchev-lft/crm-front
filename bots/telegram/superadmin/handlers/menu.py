from aiogram.types import Message

from aiogram import Router, F
from aiogram.filters import Command

from bots.telegram.superadmin.kb import sup_kb

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("ооокей", reply_markup=sup_kb)