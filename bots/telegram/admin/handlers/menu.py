from aiogram import Router, F
from aiogram.filters import Command

from aiogram.types import Message
from bots.telegram.admin.kb import admin_keyboard, apps_filters
from bots.telegram.async_requests.admin_async_request import get_all_apps
router = Router()

@router.message(Command("start"))
async def start_admin(message: Message):
    await message.answer("айоу",reply_markup=admin_keyboard)

@router.message(F.text == "Заявки")
async def all_apps(message: Message):
    apps  = await get_all_apps()
    if not apps :
        await message.answer("Заявки не найдены.")
        return

    for app in apps :
        msg  = (
            f"ID: {app['id']}\n"
            f"Клиент: {app['client_id']}\n"
            f"Авто: {app['car_id']}\n"
            f"Создано: {app['created_at']}\n"
            f"---\n"
        )

        await message.answer(msg, reply_markup=apps_filters)
