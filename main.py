import asyncio
from aiogram import Bot, Dispatcher
from handlers.basic import basic_router
from services.scheduler import start_sheduler
from config import Config


async def main():
    await start_sheduler()
    bot = Bot(token=Config().get_bot_token())
    dp = Dispatcher()
    dp.include_router(basic_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
