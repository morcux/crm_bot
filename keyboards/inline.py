from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def generate_channels_keyboard(channels):
    keyboard = []
    for channel in channels:
        keyboard.append(
            [InlineKeyboardButton(text=channel[-1],
                                 callback_data=f"channel_{channel[-2]}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


back_button = InlineKeyboardBuilder(markup=[
    [
        InlineKeyboardButton(text="В меню", callback_data="back")
    ]
])
