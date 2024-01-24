import json
import requests
from requests import Response
from config import Config


class DataProcessor:
    def __init__(self) -> None:
        self.token = Config().get_api_token()
        self.base_url = "https://fbtool.pro/api"

    def get_response(self, acc_id: int):
        url = f"{self.base_url}/get-statistics?key={self.token}&account={acc_id}&mode=adsets"
        response = requests.get(url)
        print(response.text)
        return response

    def get_spend_by_name(self, target_name: str, response: Response):
        if response.json():
            total_spend = 0
            for account in response.json()["data"]:
                
                adsets_data = account.get("adsets", {}).get("data", [])
                for adset in adsets_data:
                    if adset.get("campaign", {}).get("name") == target_name:
                        insights = adset.get("insights", [])
                        if insights:
                            print(insights["data"][0]["spend"])
                            total_spend += float(insights["data"][0]["spend"])
            print(total_spend)
            return total_spend
        return None

    def get_all_accounts(self):
        url = f"{self.base_url}/get-accounts?key={self.token}&account=17233976"
        response = requests.get(url)
        data = response.json()
        ids = [item['id'] for item in data.values() if isinstance(item, dict) and 'id' in item]
        return ids
