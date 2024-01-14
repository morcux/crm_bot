from aiogram import F, Router, Bot
from aiogram.types import Message, ChatMemberUpdated
from keyboards.reply import main_keyboard
from keyboards.inline import generate_channels_keyboard
from services.db import AsyncDatabaseHandler
from services.google_sheets import GoogleSheetEditor

basic_router = Router()


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
    print(chat_member.new_chat_member.user.id)
    user_id = chat_member.new_chat_member.user.id
    db = AsyncDatabaseHandler()
    editor = GoogleSheetEditor()
    invite_link = chat_member.invite_link
    if invite_link:
        await db.add_user(url=invite_link.invite_link,
                          user_id=user_id)
        return editor.update_mambers_count(link=invite_link.invite_link,
                                           number=1)
    is_sub = await db.check_user_by_id(user_id=user_id)
    if is_sub:
        editor.update_mambers_count(link=is_sub, number=-1)
        return await db.delete_user_by_id(user_id=user_id)


@basic_router.message(F.text == "test")
async def test(message: Message):
    print(123)
    db = AsyncDatabaseHandler()
    editor = GoogleSheetEditor()
    invite_link = None
    if invite_link:
        await db.add_user(url=invite_link,
                          user_id=message.from_user.id)
        return editor.update_mambers_count(link=invite_link,
                                           number=1)
    print(312)
    is_sub = await db.check_user_by_id(user_id=message.from_user.id)
    if is_sub:
        editor.update_mambers_count(link=is_sub, number=-1)
        return await db.delete_user_by_id(user_id=message.from_user.id)
