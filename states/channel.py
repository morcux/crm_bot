from aiogram.fsm. state import State, StatesGroup


class ChannelStates(StatesGroup):
    get_channel = State()
    get_names = State()
    get_user = State()
