from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Сгенерировать ссылки")
    ],
    [
        KeyboardButton(text="Добавить канал")
    ]
], resize_keyboard=True)
