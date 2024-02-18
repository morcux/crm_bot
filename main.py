import asyncio
from aiogram import Bot, Dispatcher
from handlers.basic import basic_router
from handlers.channel import channel_router
from handlers.url_generate import url_router
from services.scheduler import start_scheduler
from services.db import AsyncDatabaseHandler
from config import Config


async def main():
    db = AsyncDatabaseHandler()
    await db.create_tables()
    await start_scheduler()
    bot = Bot(token=Config().get_bot_token())
    dp = Dispatcher()
    dp.include_router(basic_router)
    dp.include_router(channel_router)
    dp.include_router(url_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
