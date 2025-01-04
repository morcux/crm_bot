import aiohttp
from datetime import datetime
from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from states.channel import ChannelStates
from services.db import AsyncDatabaseHandler
from keyboards.inline import generate_channels_keyboard, generate_url_keyboard

url_router = Router()

ADMIN_ID = [7544120155, 5198857407, 7109898533, 6770144323, 7107711151, 6486787455]


@url_router.callback_query(F.data.startswith("channel"))
async def get_names(call: CallbackQuery, state: FSMContext):
    channel = int(call.data.split("_")[-1])
    await call.message.answer(
        text="Введите названия для ссылок с начала строки")
    await state.set_state(ChannelStates.get_names)
    await state.update_data({"channel": channel})


@url_router.message(StateFilter(ChannelStates.get_names))
async def add_data(message: Message, state: FSMContext, bot: Bot):
    db = AsyncDatabaseHandler()
    data = await state.get_data()
    links = []
    names = message.text.split("\n")
    for i in range(len(names)):
        link = await bot.create_chat_invite_link(chat_id=data["channel"],
                                                 name=f"{names[i]}",
                                                 creates_join_request=True)
        links.append(link.invite_link)
        await db.add_url(channel_id=data["channel"],
                         url=link.invite_link)
    params = {'links': ','.join(links), 'names': ','.join(names)}
    async with aiohttp.ClientSession() as session:
        await session.get(url="http://127.0.0.1:8000/add_links", params=params)
    await message.answer(text="\n".join(links))
    await state.clear()


@url_router.message(F.text == "Удалить ссылку")
async def get_url_channel(message: Message):
    db = AsyncDatabaseHandler()
    channels = await db.get_user_url(user_id=message.from_user.id)
    if message.from_user.id in ADMIN_ID:
        channels = await db.get_all_channels()
    if not channels:
        return await message.answer("У вас нету доступа ни к одному каналу")
    keyboard = generate_channels_keyboard(channels, prefix="c_url")
    await message.answer("Выберите канал из которого удалить ссылку",
                         reply_markup=keyboard)


@url_router.callback_query(F.data.startswith("c_url"))
async def get_url(call: CallbackQuery, state: FSMContext):
    db = AsyncDatabaseHandler()
    channel_id = int(call.data.split("_")[-1])
    urls = await db.get_all_urls(channel_id=channel_id)
    keyboard = generate_url_keyboard(urls)
    await call.message.delete()
    await call.message.answer(text="Выберите ссылку",
                              reply_markup=keyboard)
    await state.update_data({"channel": channel_id})


@url_router.callback_query(F.data.startswith("url"))
async def delete_url(call: CallbackQuery, state: FSMContext, bot: Bot):
    db = AsyncDatabaseHandler()
    url = call.data.split("_", 1)[-1]
    channel_id = (await state.get_data())["channel"]
    await db.delete_url(url)
    await bot.edit_chat_invite_link(chat_id=channel_id,
                                    invite_link=url,
                                    expire_date=datetime.now())
    await call.message.answer("Ссылка была деактивирована")
    await call.message.delete()


@url_router.message(F.text == "Показать ссылки")
async def channel(message: Message):
    db = AsyncDatabaseHandler()
    channels = await db.get_user_url(user_id=message.from_user.id)
    if not channels:
        return await message.answer("У вас нету доступа ни к одному каналу")
    keyboard = generate_channels_keyboard(channels, prefix="show")
    await message.answer(text="Выберите канал", reply_markup=keyboard)


@url_router.message(F.data.startswith("show"))
async def show_urls(call: CallbackQuery):
    db = AsyncDatabaseHandler()
    channel_id = int(call.data.split("_")[-1])
    urls = await db.get_all_urls(channel_id=channel_id)
    text = ""
    for url in urls:
        text += f"{url[-1]}\n"
    await call.answer()
    await call.message.answer(text=text)
