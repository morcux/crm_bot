from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.api import DataProcessor
from services.google_sheets import GoogleSheetEditor


async def main():
    print(123)
    editor = GoogleSheetEditor()
    data_processor = DataProcessor()
    max_row_number = editor.get_last_row()
    response = data_processor.get_response()
    for row_number in range(2, max_row_number + 1):
        name = editor.get_data_by_cell(f"B{row_number}")[0][0]
        spend = data_processor.get_spend_by_name(target_name=name,
                                                 response=response)
        print(spend)
        editor.update_data("F", row_number, spend)


async def start_sheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, 'interval', minutes=1)
    scheduler.start()
