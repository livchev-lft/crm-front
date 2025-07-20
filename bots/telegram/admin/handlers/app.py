from aiogram import Router
from bots.telegram.admin.admin_bot import admin_bot
from aiogram.types import Message

from bots.telegram.async_requests.admin_async_request import get_app_for_admin
from bots.telegram.admin.kb import new_app_admin
ADMIN_CHAT_ID = 315590032
router = Router()

async def send_for_admin(app_id: int, message: Message):
    app = await get_app_for_admin(app_id)
    if not app:
        await message.answer("Ошибка при получении данных заявки")
        return
    try:
        text = (
            f"🆕 Новая заявка #{app['app_id']}\n"
            f"🚗 Машина: {app['brand']} {app['model']} ({app['year']})\n"
            f"🔢 Номер: {app['number']}\n"
            f"📞 Контакт: {app['phone']}\n"
            f"🙎‍♂️ Связь в тг: {app['client_id']}\n"
            f"📋 Проблема: {app['problem']}\n"
            f"🧭 Связь: {'Telegram' if app['conn'] == 0 else 'Телефон'}"
        )
        keyboard = new_app_admin(app_id, app['client_id'])
        await admin_bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except KeyError as e:
        await message.answer(f"❌ Ошибка при обработке данных: отсутствует поле {e}")

