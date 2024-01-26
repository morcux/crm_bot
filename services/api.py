import re
import json
import aiohttp
import asyncio
from aiohttp import ClientResponse
from config import Config


class DataProcessor:
    def __init__(self) -> None:
        self.token = Config().get_api_token()
        self.base_url = "https://fbtool.pro/api"

    async def get_response(self, acc_id: int) -> ClientResponse:
        url = f"{self.base_url}/get-statistics?key={self.token}&account={acc_id}&mode=adsets"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                try:
                    data = json.loads(await response.text())
                except json.decoder.JSONDecodeError:
                    asyncio.sleep(10)
                    await self.get_response(acc_id=acc_id)
                return 

    async def get_spend_by_name(self, target_name: str, response) -> float:
        total_spend = 0
        data = response
        
        for account in data.get("data", []):
            adsets_data = account.get("adsets", {}).get("data", [])
            for adset in adsets_data:
                if re.sub(r'(\\u[0-9a-fA-F]{4})', lambda x: bytes(x.group(1), 'utf-8').decode('unicode_escape'),
                            adset.get("campaign", {}).get("name")) == target_name:
                    
                    insights = adset.get("insights", [])
                    if insights:
                        print(insights["data"][0]["spend"])
                        total_spend += float(insights["data"][0]["spend"])
        if total_spend > 0.0:
            return total_spend
        return None

    async def get_all_accounts(self) -> list:
        url = f"{self.base_url}/get-accounts?key={self.token}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = json.loads(await response.text())
                ids = [item['id'] for item in data.values() if isinstance(item, dict) and 'id' in item]
                return ids
