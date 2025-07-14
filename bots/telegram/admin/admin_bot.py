import asyncio
import os

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from bots.telegram.admin.handlers import app, menu

load_dotenv()
admin_bot = Bot(token=os.environ.get("ADMIN_BOT_TOKEN"))

async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(app.router)
    dp.include_router(menu.router)
    await asyncio.gather(
        dp.start_polling(admin_bot),
    )

if __name__ == "__main__":
    asyncio.run(main())