import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.api import DataProcessor
from services.google_sheets import GoogleSheetEditor


async def main():
    editor = GoogleSheetEditor()
    data_processor = DataProcessor()
    accounts = await data_processor.get_all_accounts()
    data = editor.get_all_sheet_data()
    rows = [[row[0], row[1], row[-3], row[-1]] if len(row) == 11 else [row[0], row[1], row[-3], ""] for row in data]
    for row in rows:

        if row[-1] != "":
            response = await data_processor.get_response(acc_id=row[-1])
            spend = await data_processor.get_spend_by_name(target_name=row[1],
                                                        response=response)
            editor.update_data("F", row[0], spend)
            continue
        for account in accounts:
            print(account)
            response = await data_processor.get_response(acc_id=account)
            spend = await data_processor.get_spend_by_name(target_name=row[1],
                                                           response=response)
            if spend is None:
                continue
            editor.update_data(colm="K", number=row[0], value=account)
            editor.update_data("F", row[0], spend)
            break
        if spend is None:
            editor.update_data("F", row[0], "Не найдено")
            
    
async def links_migration():
    editor = GoogleSheetEditor()
    data = editor.get_all_sheet_data()

    next_day = datetime.datetime.today() + datetime.timedelta(days=1)
    new_name = next_day.strftime("%d/%m/%Y")

    ws = editor.create_new_sheet(name=new_name)
    editor.add_data(data=data, sheet=ws)


async def start_sheduler():
    # await main()
    # await links_migration()S
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(main, 'interval', minutes=30)
    scheduler.add_job(links_migration, "cron", hour=23, minute=59)
    scheduler.start()
