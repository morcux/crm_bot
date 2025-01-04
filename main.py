import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers.basic import basic_router
from handlers.channel import channel_router
from handlers.url_generate import url_router
from handlers.search import search_router
from handlers.url_permission import permission_router
from services.scheduler import start_scheduler
from services.db import AsyncDatabaseHandler
from config import Config

logging.basicConfig(level=logging.INFO)


async def main():
    db = AsyncDatabaseHandler()
    await db.create_tables()
    await start_scheduler()
    bot = Bot(token=Config().get_bot_token())
    info_bot = Bot(token=Config().get_info_bot_token())
    dp = Dispatcher()
    dp.include_router(basic_router)
    dp.include_router(channel_router)
    dp.include_router(url_router)
    dp.include_router(permission_router)
    tasks = []
    await bot.delete_webhook()
    bot_task = asyncio.create_task(dp.start_polling(bot))
    tasks.append(bot_task)
    dp_info = Dispatcher()
    dp_info.include_router(search_router)
    info_task = asyncio.create_task(dp_info.start_polling(info_bot))
    tasks.append(info_task)
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
