import asyncio
import os

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from bots.telegram.superadmin.handlers import menu

load_dotenv()
superadmin_bot = Bot(token=os.environ.get("SUPERADMIN_BOT_TOKEN"))

async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(menu.router)
    await asyncio.gather(
        dp.start_polling(superadmin_bot)
    )

if __name__ == "__main__":
    asyncio.run(main())