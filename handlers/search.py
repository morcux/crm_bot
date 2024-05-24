from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.channel import Manager
from services.db import AsyncDatabaseHandler
from keyboards.inline import generate_channels_keyboard
from keyboards.reply import admin_menu, search_keyboard

ADMIN_ID = 123123

search_router = Router()

@search_router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == ADMIN_ID:
        keyboard = admin_menu
    else:
        keyboard = search_keyboard
    await message.answer("Добро пожаловать!", reply_markup=keyboard)

@search_router.message(F.text == "Добавить менеджера")
async def add_manager(message: Message):
    db = AsyncDatabaseHandler()
    channels = await db.get_all_channels()
    keyboard = generate_channels_keyboard(channels, "manager_add")
    await message.answer("Выберите канал в который добавить менеджера",
                         reply_markup=keyboard)
    

@search_router.callback_query(F.data.startswith("manager_add"))
async def get_manager_id(call: CallbackQuery, state: FSMContext):
    channel_id = call.data.split("_")[-1]
    await state.set_state(Manager.add_user_id)
    await call.message.answer("Введите айди менеджера")
    await state.update_data({"channel_id": channel_id})
    await call.message.delete()


@search_router.message(Manager.add_user_id)
async def add_manager(message: Message, state: FSMContext):
    db = AsyncDatabaseHandler()
    data = await state.get_data()
    await db.add_permission(user_id=message.text, channel_id=data["channel_id"])
    await message.answer("Менеджера добавлено!")
    await state.clear()

@search_router.message(F.text == "Удалить менеджера")
async def delete_manager(message: Message):
    db = AsyncDatabaseHandler()
    channels = await db.get_all_channels()
    keyboard = generate_channels_keyboard(channels, "manager_delete")
    await message.answer("Выберите канал с которого удалить менеджера",
                         reply_markup=keyboard)
    

@search_router.callback_query(F.data.startswith("manager_delete"))
async def get_manager_id_to_delete(call: CallbackQuery, state: FSMContext):
    channel_id = call.data.split("_")[-1]
    await state.set_state(Manager.delete_user_id)
    await call.message.answer("Введите айди менеджера")
    await state.update_data({"channel_id": channel_id})
    await call.message.delete()

@search_router.message(Manager.delete_user_id)
async def delete_manager(message: Message, state: FSMContext):
    db = AsyncDatabaseHandler()
    data = await state.get_data()
    await db.delete_permission(user_id=message.text, channel_id=data["channel_id"])
    await message.answer("Менеджера удалено!")
    await state.clear()

@search_router.message(F.text == "Поиск")
async def search_user(message: Message):
    db = AsyncDatabaseHandler()
    channels = await db.get_user_channels(user_id=message.from_user.id)
    print(channels)
    if not channels:
        await message.answer("У вас нет доступа ни к одному каналу.")
        return

    keyboard = generate_channels_keyboard(channels, prefix="search")
    await message.answer("Выберите канал, в котором искать", reply_markup=keyboard)

    
@search_router.callback_query(F.data.startswith("search"))
async def get_id(call: CallbackQuery, state: FSMContext):
    channel_id = call.data.split("_")[-1]
    await state.set_state(Manager.search)
    await state.update_data({"channel_id": channel_id})
    await call.message.answer("Введите айди человека")
    await call.message.delete()

@search_router.message(Manager.search)
async def get_info(message: Message, state: FSMContext):
    db = AsyncDatabaseHandler()
    data = await state.get_data()
    
    user_id = message.text
    channel_id = data["channel_id"]
    print(user_id, channel_id)
    subscriptions = await db.get_subscriptions(user_id=user_id, channel_id=channel_id)
    print(subscriptions)
    if not subscriptions:
        return await message.answer("Пользователя не найдено")
    
    subscription = subscriptions[0]
    url_name, timestamp = subscription

    await message.answer(text=f"Название ссылки: {url_name}\nВремя присоединения: {timestamp}")
