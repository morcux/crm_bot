import aiohttp
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.google_sheets import GoogleSheetEditor


async def main():
    async with aiohttp.ClientSession() as session:
        await session.get("http://127.0.0.1:8000/spends")


async def links_migration():
    editor = GoogleSheetEditor()
    data = editor.get_all_sheet_data()
    for row in data:
        row[5] = 0
        row[6] = 0

    next_day = datetime.datetime.today() + datetime.timedelta(days=1)
    new_name = next_day.strftime("%d/%m/%Y")

    ws = editor.create_new_sheet(name=new_name)
    editor.add_data(data=data, sheet=ws)


async def start_scheduler():
    # await main()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(main, 'interval', minutes=30)
    scheduler.add_job(links_migration, "cron", hour=23, minute=59)
    scheduler.start()
