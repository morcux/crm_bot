from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from services.db import AsyncDatabaseHandler
from keyboards.inline import generate_channels_keyboard
from states.channel import Buyer

permission_router = Router()


@permission_router.message(F.text == "Добавить баера")
async def add_buyer(message: Message):
    db = AsyncDatabaseHandler()
    channels = await db.get_all_channels()
    keyboard = generate_channels_keyboard(channels, "buyer_add")
    await message.answer("Выберите канал в который добавить баера",
                         reply_markup=keyboard)


@permission_router.callback_query(F.data.startswith("buyer_add"))
async def get_buyer_id(call: CallbackQuery, state: FSMContext):
    channel_id = call.data.split("_")[-1]
    await state.set_state(Buyer.add_user_id)
    await call.message.answer("Введите айди баера")
    await state.update_data({"channel_id": channel_id})
    await call.message.delete()


@permission_router.message(Buyer.add_user_id)
async def add_man(message: Message, state: FSMContext):
    db = AsyncDatabaseHandler()
    data = await state.get_data()
    await db.add_permission_url(user_id=message.text,
                                channel_id=data["channel_id"])
    await message.answer("Баера добавлено!")
    await state.clear()


@permission_router.message(F.text == "Удалить баера")
async def delete_buyer(message: Message):
    db = AsyncDatabaseHandler()
    channels = await db.get_all_channels()
    keyboard = generate_channels_keyboard(channels, "buyer_delete")
    await message.answer("Выберите канал с которого удалить баера",
                         reply_markup=keyboard)


@permission_router.callback_query(F.data.startswith("buyer_delete"))
async def get_buyer_id_to_delete(call: CallbackQuery, state: FSMContext):
    channel_id = call.data.split("_")[-1]
    await state.set_state(Buyer.delete_user_id)
    await call.message.answer("Введите айди баера")
    await state.update_data({"channel_id": channel_id})
    await call.message.delete()


@permission_router.message(Buyer.delete_user_id)
async def del_Buyer(message: Message, state: FSMContext):
    db = AsyncDatabaseHandler()
    data = await state.get_data()
    await db.delete_permission_url(user_id=message.text,
                                   channel_id=data["channel_id"])
    await message.answer("Баера удалено!")
    await state.clear()
