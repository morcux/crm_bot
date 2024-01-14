from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from states.channel import ChannelStates
from services.db import AsyncDatabaseHandler

channel_router = Router()


@channel_router.message(F.text == "Добавить канал")
async def get_channel(message: Message, state: FSMContext):
    await message.answer(text="Введите айди каналов с новой строки")
    await state.set_state(ChannelStates.get_channel)


@channel_router.message(StateFilter(ChannelStates.get_channel))
async def add_channel(message: Message, state: FSMContext, bot: Bot):
    channels = message.text.split("\n")
    db = AsyncDatabaseHandler()
    for channel in channels:
        try:
            channel = await bot.get_chat(chat_id=channel)
            await db.add_channel(channel_id=channel.id,
                                 channel_name=channel.full_name)
            await message.answer(text=f"Канал {channel.full_name} добавлено")
        except TelegramBadRequest:
            await message.answer(text="Не удалось добавить канал, возможно бот в нем не состоит")
