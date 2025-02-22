from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


languages = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="UZB"),
            KeyboardButton(text="RUS"),
            KeyboardButton(text="ENG")
        ]

    ],
    resize_keyboard=True
)
menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Testni Boshlash"),
            KeyboardButton(text="Tarix")
        ]
    ],
    resize_keyboard=True
)