from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Сгенерировать ссылки")
    ],
    [
        KeyboardButton(text="Удалить ссылку")
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

admin_crm_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Добавить баера"),
        KeyboardButton(text="Удалить баера")
    ],
    [
        KeyboardButton(text="Сгенерировать ссылки"),
        KeyboardButton(text="Удалить ссылку")
    ],
    [
        KeyboardButton(text="Добавить канал"),
        KeyboardButton(text="Удалить канал")
    ]
], resize_keyboard=True)
