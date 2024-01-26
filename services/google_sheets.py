import datetime
import gspread
from gspread import Worksheet
from typing import List
from config import Config


client = gspread.service_account(filename=Config().get_client_secret_path())
sh = client.open_by_key("1c63VemrYWl1ZLgkO5tpo0860qfKRxdTKMmoP3B7S8CU")


class GoogleSheetEditor():

    def create_new_sheet(self, name: str):
        ws = sh.add_worksheet(title=name, rows=10000, cols=100, index=0)
        return ws

    def get_worksheet(self):
        ws = sh.get_worksheet(0)
        date = datetime.datetime.today().strftime("%d/%m/%Y")
        if ws.title != date:
            try:
                ws = self.create_new_sheet(name=date)
            except gspread.exceptions.APIError:
                current = 0
                while True:
                    ws = sh.get_worksheet(current)
                    if ws.title == date:
                        return ws
                    current += 1
        return ws

    def get_last_row(self):
        wks = self.get_worksheet()
        return len(wks.get_all_values())

    def update_data(self, colm: str, number: int, value: str):
        wks = self.get_worksheet()
        wks.update(f'{colm}{number}', [[value]])

    def add_data(self, data: list, sheet: Worksheet):
        sheet.update(data)

    def find_by_data(self, data: str):
        wks = self.get_worksheet()
        return wks.find(query=data)

    def add_links(self, links: List[str], names: List[str], users: List[str]):
        wks = self.get_worksheet()
        start_row = self.get_last_row() + 1
        for i in range(len(links)):
            wks.update(
                range_name=f"A{start_row}",
                values=[
                    [start_row,
                     names[i], "", "", "", "", 0, 0, links[i], users[i]]
                       ])
            start_row += 1

    def get_data_by_cell(self, cell: str):
        wks = self.get_worksheet()
        # print(wks.get(cell))
        return wks.get(cell)

    def update_mambers_count(self, link: str, number: int):
        cell = self.find_by_data(data=link)
        if cell:
            current = self.get_data_by_cell(cell=f"G{cell.row}")
            if current:
                self.update_data(colm="G", number=cell.row,
                                value=int(current[0][0])+number)

    def get_all_sheet_data(self):
        wks = self.get_worksheet()
        return wks.get_all_values()
