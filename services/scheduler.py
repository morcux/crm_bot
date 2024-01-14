import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.api import DataProcessor
from services.google_sheets import GoogleSheetEditor


async def main():
    editor = GoogleSheetEditor()
    data_processor = DataProcessor()
    accounts = data_processor.get_all_accounts()
    max_row_number = editor.get_last_row()
    for row_number in range(2, max_row_number + 1):
        name = editor.get_data_by_cell(f"B{row_number}")[0][0]
        for account in accounts:
            response = data_processor.get_response(acc_id=account)
            spend = data_processor.get_spend_by_name(target_name=name,
                                                     response=response)
            if spend is None:
                continue
            else:
                break
        print(spend)
        editor.update_data("F", row_number, spend)


def links_migration():
    editor = GoogleSheetEditor()
    data = editor.get_all_sheet_data()

    next_day = datetime.datetime.today() + datetime.timedelta(days=1)
    new_name = next_day.strftime("%d/%m/%Y")

    ws = editor.create_new_sheet(name=new_name)
    editor.add_data(data=data, sheet=ws)


async def start_sheduler():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(main, 'interval', minutes=1)
    scheduler.add_job(links_migration, "cron", hour=20, minute=34)
    scheduler.start()
