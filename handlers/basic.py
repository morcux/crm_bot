import aiohttp
from aiogram import F, Router, Bot
from aiogram.types import Message, ChatMemberUpdated
from keyboards.reply import main_keyboard, admin_crm_menu
from keyboards.inline import generate_channels_keyboard
from services.fb import send_facebook_event
from services.db import AsyncDatabaseHandler

basic_router = Router()

ADMIN_ID = [6426165426, 5198857407]


@basic_router.message(F.text == "/start")
async def start(message: Message):
    if message.from_user.id in ADMIN_ID:
        keyboard = admin_crm_menu
    else:
        keyboard = main_keyboard
    await message.answer(text="Добро пожаловать в CRM бот",
                         reply_markup=keyboard)


@basic_router.message(F.text == "Сгенерировать ссылки")
async def generate(message:  Message, bot: Bot):
    db = AsyncDatabaseHandler()
    channels = await db.get_user_url(user_id=message.from_user.id)
    if message.from_user.id in ADMIN_ID:
        channels = await db.get_all_channels()
    if not channels:
        return await message.answer("Увас нету доступа ни к одному каналу")
    keyboard = generate_channels_keyboard(channels)
    await message.answer(text="Выберите канал", reply_markup=keyboard)


@basic_router.chat_member()
async def on_chat_member_join(chat_member: ChatMemberUpdated):
    user_id = chat_member.new_chat_member.user.id
    db = AsyncDatabaseHandler()
    invite_link = chat_member.invite_link
    if chat_member.chat.id == -1002106220236:
        await send_facebook_event("Subscribe", user_id)
    if invite_link is not None:
        await db.add_subscription(user_id=user_id,
                                  url_name=invite_link.name,
                                  channel_id=chat_member.chat.id,
                                  )
        await db.add_user(url=invite_link.invite_link,
                          user_id=user_id)
        params = {"url": invite_link.invite_link, "number": 1}
        async with aiohttp.ClientSession() as session:
            await session.get("http://127.0.0.1:8000/update_member_count",
                              params=params)
            return
    is_sub = await db.check_user_by_id(user_id=user_id)
    if is_sub is not None:
        await db.delete_permission(user_id=user_id,
                                   channel_id=chat_member.chat.id)
        await db.delete_user_by_id(user_id=user_id)
        params = {"url": is_sub, "number": -1}
        async with aiohttp.ClientSession() as session:
            await session.get("http://127.0.0.1:8000/update_member_count",
                              params=params)
