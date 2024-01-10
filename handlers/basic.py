from datetime import timedelta
from aiogram import F, Router, Bot
from aiogram.types import Message, ChatMemberUpdated
from keyboards.reply import main_keyboard
from services.google_sheets import GoogleSheetEditor
from config import Config

basic_router = Router()


@basic_router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(text="Добро пожаловать в CRM бот",
                         reply_markup=main_keyboard)


@basic_router.message(F.text == "Сгенерировать ссылки")
async def generate(message:  Message, bot: Bot):
    await message.answer(text="Генерирую...")
    channel_id = Config().get_channel_id()
    editor = GoogleSheetEditor()
    links = []
    for i in range(10):
        link = await bot.create_chat_invite_link(chat_id=channel_id,
                                                 name=f"K{i}",
                                                 creates_join_request=False,
                                                 expire_date=timedelta(days=1))
        links.append(link.invite_link)

    editor.add_links(links)
    await message.answer(text="\n".join(links))


@basic_router.chat_member(F.chat.id == int(Config().get_channel_id()))
async def on_chat_member_join(chat_member: ChatMemberUpdated):
    editor = GoogleSheetEditor()
    invite_link = chat_member.invite_link
    if invite_link:
        print(invite_link.invite_link)
        editor.update_mambers_count(link=invite_link.invite_link)
