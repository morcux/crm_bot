import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.api import DataProcessor
from services.google_sheets import GoogleSheetEditor


async def main():
    editor = GoogleSheetEditor()
    data_processor = DataProcessor()
    accounts = data_processor.get_all_accounts()
    max_row_number = editor.get_last_row()
    for row_number in range(1, max_row_number + 1):
        print(row_number)
        name = editor.get_data_by_cell(f"B{row_number}")[0][0]
        try:
            acc = editor.get_data_by_cell(f"K{row_number}")[0][0]
        except IndexError:
            acc = None
        if acc:
            response = data_processor.get_response(acc_id=acc)
            spend = data_processor.get_spend_by_name(target_name=name,
                                                     response=response)
            if spend:
                editor.update_data("F", row_number, spend)
                continue
        else:
            for account in accounts:
                response = data_processor.get_response(acc_id=account)
                spend = data_processor.get_spend_by_name(target_name=name,
                                                        response=response)
                if spend is None:
                    continue
                else:
                    editor.update_data(colm="K",
                                    number=row_number,
                                    value=account)
                    editor.update_data("F", row_number, spend)
                    
                    break


def links_migration():
    editor = GoogleSheetEditor()
    data = editor.get_all_sheet_data()

    next_day = datetime.datetime.today() + datetime.timedelta(days=1)
    new_name = next_day.strftime("%d/%m/%Y")

    ws = editor.create_new_sheet(name=new_name)
    editor.add_data(data=data, sheet=ws)


async def start_sheduler():
    # await main()
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(main, 'interval', minutes=30)
    scheduler.add_job(links_migration, "cron", hour=23, minute=59)
    scheduler.start()
