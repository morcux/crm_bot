import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.db import AsyncDatabaseHandler

async def main():
    async with aiohttp.ClientSession() as session:
        await session.get("http://127.0.0.1:8000/spends")


async def links_migration():
    db = AsyncDatabaseHandler()
    await db.delete_all_users()
    async with aiohttp.ClientSession() as session:
        await session.get("http://127.0.0.1:8000/link_migration")



async def start_scheduler():
    await main()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(main, 'interval', minutes=30)
    scheduler.add_job(links_migration, "cron", hour=23, minute=59)
    scheduler.start()
