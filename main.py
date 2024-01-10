import asyncio
from aiogram import Bot, Dispatcher
from handlers.basic import basic_router
from config import Config


async def main():
    bot = Bot(token=Config().get_bot_token())
    dp = Dispatcher()
    dp.include_router(basic_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
