import asyncio
import os

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from bots.telegram.client.handlers import auth, start, menu, cars, app

load_dotenv()
client_bot = Bot(token=os.environ.get("CLIENT_BOT_TOKEN"))

async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(auth.router)
    dp.include_router(start.router)
    dp.include_router(cars.router)
    dp.include_router(menu.router)
    dp.include_router(app.router)
    await asyncio.gather(
        dp.start_polling(client_bot),
    )

if __name__ == '__main__':
    asyncio.run(main())