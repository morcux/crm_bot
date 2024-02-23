import re
from datetime import datetime
from bs4 import BeautifulSoup
import json
import aiohttp
import asyncio
from aiohttp import ClientResponse
import pytz
from config import Config


class DataProcessor:
    def __init__(self) -> None:
        self.token = Config().get_api_token()
        self.base_url = "https://fbtool.pro/api"

    async def convert(self, spend: float, currency: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"https://www.forbes.com/advisor/money-transfer/currency-converter/{currency.lower()}-usd/?amount={spend}") as response:
                soup = BeautifulSoup(await response.text(), "html.parser")
                return soup.find("span", class_="amount")

    async def get_response(self,
                           acc_id: int,
                           retries: int = 3) -> ClientResponse:
        msk_timezone = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(msk_timezone)
        formatted_time = current_time.strftime('%Y-%m-%d')
        url = f"{self.base_url}/get-statistics?key={self.token}&account={acc_id}&mode=adsets&dates={formatted_time} - {formatted_time}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                try:
                    data = json.loads(await response.text())
                except json.decoder.JSONDecodeError:
                    print(23981)
                    if retries > 0:
                        await asyncio.sleep(10)
                        return await self.get_response(acc_id=acc_id,
                                                       retries=retries-1)
                    else:
                        raise
                print(data)
                return data

    async def get_spend_by_name(self, target_name: str, response) -> float:
        total_spend = 0
        data = response
        for account in data.get("data", []):
            currency = account.get("currency")
            adsets_data = account.get("adsets", {}).get("data", [])
            for adset in adsets_data:
                if re.sub(r'(\\u[0-9a-fA-F]{4})', lambda x: bytes(x.group(1), 'utf-8').decode('unicode_escape'), adset.get("campaign", {}).get("name")) == target_name:
                    insights = adset.get("insights", [])
                    if insights:
                        spend = insights["data"][0]["spend"]
                        if currency != "USD":
                            spend = await self.convert(spend, currency)

                        total_spend += float(spend)
                        print(spend)
        if total_spend > 0.0:
            return total_spend
        return None

    async def get_all_accounts(self) -> list:
        url = f"{self.base_url}/get-accounts?key={self.token}"
        print(123)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = json.loads(await response.text())
                print(data)
                ids = [item['id'] for item in data.values() if isinstance(item, dict) and 'id' in item]
                print(ids)
                return ids
