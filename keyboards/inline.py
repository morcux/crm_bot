from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def generate_channels_keyboard(channels):
    keyboard = InlineKeyboardBuilder()
    for channel in channels:
        keyboard.add(
            InlineKeyboardButton(text=channel[-1],
                                 callback_data=f"channel_{channel[-2]}"))
    return keyboard.as_markup()


back_button = InlineKeyboardBuilder(markup=[
    [
        InlineKeyboardButton(text="В меню", callback_data="back")
    ]
])
