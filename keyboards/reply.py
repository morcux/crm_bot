from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Сгенерировать ссылки")
    ],
    [
        KeyboardButton(text="Добавить канал")
    ]
], resize_keyboard=True)

admin_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Добавить менеджера"),
        KeyboardButton(text="Удалить менеджера")
    ],
    [
        KeyboardButton(text="Поиск")
    ]
], resize_keyboard=True)

search_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Поиск")
    ]
], resize_keyboard=True)