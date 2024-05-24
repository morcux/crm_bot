import hashlib
import json
import re
import time
import urllib
import aiohttp
from aiogram import F, Router, Bot
from aiogram.types import Message, ChatMemberUpdated
from keyboards.reply import main_keyboard
from keyboards.inline import generate_channels_keyboard
from services.db import AsyncDatabaseHandler

basic_router = Router()

def get_gtm_time():
    return int(time.mktime(time.gmtime()))


def remove_special_characters(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    return text


def get_sha256_hash(string, lower):
    if lower:
        string = string.lower()

    return hashlib.sha256(string.encode()).hexdigest()


@basic_router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(text="Добро пожаловать в CRM бот",
                         reply_markup=main_keyboard)


@basic_router.message(F.text == "Сгенерировать ссылки")
async def generate(message:  Message, bot: Bot):
    db = AsyncDatabaseHandler()
    channels = await db.get_all_channels()
    keyboard = generate_channels_keyboard(channels)
    await message.answer(text="Выберите канал", reply_markup=keyboard)


@basic_router.chat_member()
async def on_chat_member_join(chat_member: ChatMemberUpdated):
    print("SUB")
    user_id = chat_member.new_chat_member.user.id
    db = AsyncDatabaseHandler()
    invite_link = chat_member.invite_link
    if invite_link is not None:
        print(invite_link.invite_link)
        await db.add_user(url=invite_link.invite_link,
                          user_id=user_id)
        params = {"url": invite_link.invite_link, "number": 1}
        async with aiohttp.ClientSession() as session:
            print(params)
            response = await session.get("http://127.0.0.1:8000/update_member_count", params=params)
            print(response)
        user = chat_member.from_user
        async with aiohttp.ClientSession() as session:
            compaigns = await session.get(
                "http://91.210.166.88/admin_api/v1/campaigns",
                headers={'Api-Key': "ca0afac2590622c1e8237974e2f413d3"})
            compaigns = await compaigns.json()
            current_compaign = None
            for compaign in compaigns:
                if compaign["parameters"] != []:
                    try:
                        if compaign["parameters"]["sub_id_1"]:
                            if compaign["parameters"]["sub_id_1"]["placeholder"] == invite_link:
                                current_compaign = compaign
                                break
                    except KeyError as e:
                        print(e)
                        print(compaign["parameters"])
                        continue
            if current_compaign is None:
                print(current_compaign)
                return
            domain = current_compaign["domain"]
            body = {
                "data": [{
                    "event_name": "Subscribe",
                    "event_time": get_gtm_time(),
                    "event_source_url": urllib.parse.quote(f'{domain}'),
                    "user_data": {
                        "external_id": current_compaign["parameters"]["external_id"]["placeholder"],
                    }
                }]
            }
            if user.first_name:
                body['data'][0]['user_data']['fn'] = get_sha256_hash(remove_special_characters(user.first_name).strip(), True)

            if user.last_name:
                body['data'][0]['user_data']['ln'] = get_sha256_hash(remove_special_characters(user.last_name).strip(), True)

            pixel_id = current_compaign["parameters"]["sub_id_7"]["placeholder"]
            pixel_token = current_compaign["parameters"]["sub_id_15"]["placeholder"]
            url = f"https://graph.facebook.com/v15.0/{pixel_id}/events?access_token={pixel_token}"
            response = await session.post(url,
                                        data=json.dumps(body).encode("utf-8"),
                                        headers={"Content-Type": "application/json"})
            print(await response.json())    
            return
    is_sub = await db.check_user_by_id(user_id=user_id)
    if is_sub is not None:
        await db.delete_user_by_id(user_id=user_id)
        params = {"url": is_sub, "number": -1}
        async with aiohttp.ClientSession() as session:
            await session.get("http://127.0.0.1:8000/update_member_count", params=params)