from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from states.channel import ChannelStates
from services.db import AsyncDatabaseHandler
from keyboards.inline import generate_channels_keyboard

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
    await state.clear()


@channel_router.message(F.text == "Удалить канал")
async def delete_channel(message: Message):
    db = AsyncDatabaseHandler()
    channels = await db.get_all_channels()
    keyboard = generate_channels_keyboard(channels=channels,
                                          prefix="del_channel")
    await message.answer("Выберите канал который удалить",
                         reply_markup=keyboard)


@channel_router.callback_query(F.data.startswith("del_channel"))
async def del_channel(call: CallbackQuery):
    channel_id = call.data.split("_")[-1]
    db = AsyncDatabaseHandler()
    await db.delete_channel_by_id(channel_id=channel_id)
    await call.answer()
    await call.message.answer("Канала удалён")
    await call.message.delete()
