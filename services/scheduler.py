import asyncio
import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.db import AsyncDatabaseHandler


async def start_main():
    print("start")
    asyncio.create_task(main())

async def main():
    print("send")
    async with aiohttp.ClientSession() as session:
        print("send2")
        await session.get("http://127.0.0.1:8000/spends")
        print("send3")
        


async def links_migration():
    db = AsyncDatabaseHandler()
    await db.delete_all_users()
    async with aiohttp.ClientSession() as session:
        await session.get("http://127.0.0.1:8000/link_migration")



async def start_scheduler():
    await start_main()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(start_main, 'interval', minutes=60)
    scheduler.add_job(links_migration, "cron", hour=23, minute=59)
    scheduler.start()
