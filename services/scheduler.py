import aiohttp
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def main():
    async with aiohttp.ClientSession() as session:
        await session.get("http://127.0.0.1:8000/spends")


async def links_migration():
    async with aiohttp.ClientSession() as session:
        await session.get("http://127.0.0.1:8000/link_migration")


async def start_scheduler():
    # await links_migration()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(main, 'interval', minutes=30)
    scheduler.add_job(links_migration, "cron", hour=23, minute=59)
    scheduler.start()
