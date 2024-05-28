import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    def __init__(self) -> None:
        self.__BOT_TOKEN = os.getenv("BOT_TOKEN", default="")
        self.__INFO_BOT_TOKEN = os.getenv("INFO_BOT_TOKEN", default="")
        self.__CLIENT_SECRET_PATH = os.getenv("CLIENT_SECRET_PATH", default="")
        self.__API_TOKEN = os.getenv("API_TOKEN", default="")
        self.__CHANNEL_ID = os.getenv("CHANNEL_ID", default=123)
        self.__FB_TOKEN = os.getenv("FB_TOKEN", default="")

    def get_bot_token(self):
        return self.__BOT_TOKEN

    def get_client_secret_path(self):
        return self.__CLIENT_SECRET_PATH

    def get_api_token(self):
        return self.__API_TOKEN

    def get_channel_id(self):
        return self.__CHANNEL_ID

    def get_info_bot_token(self):
        return self.__INFO_BOT_TOKEN

    def get_fb_token(self):
        return self.__FB_TOKEN