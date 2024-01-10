import gspread
from typing import List
from config import Config


client = gspread.service_account(filename=Config().get_client_secret_path())
sh = client.open_by_key("1c63VemrYWl1ZLgkO5tpo0860qfKRxdTKMmoP3B7S8CU")
wks = sh.sheet1


class GoogleSheetEditor():

    def update_data(self, colm: str, number: int, value: str):
        wks.update(f'{colm}{number}', [[value]])

    def find_by_data(self, data: str):
        return wks.find(query=data)

    def add_links(self, links: List[str]):
        start_row = len(wks.get_all_values()) + 1
        for link in links:
            wks.update(
                range_name=f"A{start_row}",
                values=[
                    [start_row, f"K{start_row}", "", "", "", "", "0", "", link]
                       ])
            start_row += 1

    def update_mambers_count(self, link: str):
        cell = self.find_by_data(data=link)
        current = wks.get(f"G{cell.row}")
        self.update_data(colm="G", number=cell.row, value=int(current[0][0])+1)
