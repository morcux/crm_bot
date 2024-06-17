from aiogram.fsm. state import State, StatesGroup


class ChannelStates(StatesGroup):
    get_channel = State()
    get_names = State()
    get_user = State()


class Manager(StatesGroup):
    add_user_id = State()
    delete_user_id = State()
    search = State()


class Buyer(StatesGroup):
    add_user_id = State()
    delete_user_id = State()
