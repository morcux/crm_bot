import datetime
import gspread
from typing import List
from config import Config


client = gspread.service_account(filename=Config().get_client_secret_path())
sh = client.open_by_key("1c63VemrYWl1ZLgkO5tpo0860qfKRxdTKMmoP3B7S8CU")


class GoogleSheetEditor():

    def get_worksheet(self):
        ws = sh.get_worksheet(-1)
        date = datetime.datetime.today().strftime("%d/%m/%Y")
        if ws.title != date:
            ws = sh.add_worksheet(title=date, rows=100, cols=100)
        return ws

    def get_last_row(self):
        wks = self.get_worksheet()
        return len(wks.get_all_values())

    def update_data(self, colm: str, number: int, value: str):
        wks = self.get_worksheet()
        wks.update(f'{colm}{number}', [[value]])

    def find_by_data(self, data: str):
        wks = self.get_worksheet()
        return wks.find(query=data)

    def add_links(self, links: List[str]):
        wks = self.get_worksheet()
        start_row = self.get_last_row() + 1
        for link in links:
            wks.update(
                range_name=f"A{start_row}",
                values=[
                    [start_row, f"K{start_row}", "", "", "", "", "0", "", link]
                       ])
            start_row += 1

    def get_data_by_cell(self, cell: str):
        wks = self.get_worksheet()
        print(wks.get(cell))
        return wks.get(cell)

    def update_mambers_count(self, link: str):
        cell = self.find_by_data(data=link)
        current = self.get_data_by_cell()
        self.update_data(colm="G", number=cell.row, value=int(current[0][0])+1)
