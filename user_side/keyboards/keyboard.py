from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from user_side.translations.translation import translate_into

def get_languages_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🇺🇿 Uz"),
                KeyboardButton(text="🇺🇸 Eng"),
                KeyboardButton(text="🇷🇺 Ru")
            ]
        ],
        resize_keyboard=True
    )

def get_menu_keyboard(data):
    path = "user_side/translations/keyboard_translations.json"
    translations = translate_into(path, data)
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=translations["menu"]["start_test"][data['current_language']]),
                KeyboardButton(text=translations["menu"]["history"][data['current_language']])
            ]
        ],
        resize_keyboard=True
    )

def get_relationship_keyboard(data):
    path = "user_side/translations/keyboard_translations.json"
    translations = translate_into(path, data)
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=translations["relationship"]["father"][data['current_language']]),
                KeyboardButton(text=translations["relationship"]["mother"][data['current_language']])
            ],
            [
                KeyboardButton(text=translations["relationship"]["other"][data['current_language']]),
                KeyboardButton(text=translations["relationship"]["back_to_main"][data['current_language']])
            ]
        ],
        resize_keyboard=True
    )

def get_months_keyboard(data):
    path = "user_side/translations/keyboard_translations.json"
    translations = translate_into(path, data)
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=translations["months"]["1_month"][data['current_language']]),
                KeyboardButton(text=translations["months"]["2_month"][data['current_language']]),
                KeyboardButton(text=translations["months"]["3_month"][data['current_language']])
            ],
            [
                KeyboardButton(text=translations["months"]["4_month"][data['current_language']]),
                KeyboardButton(text=translations["months"]["5_month"][data['current_language']]),
                KeyboardButton(text=translations["months"]["6_month"][data['current_language']])
            ],
            [
                KeyboardButton(text=translations["months"]["7_month"][data['current_language']]),
                KeyboardButton(text=translations["months"]["8_month"][data['current_language']]),
                KeyboardButton(text=translations["months"]["9_month"][data['current_language']])
            ],
            [
                KeyboardButton(text=translations["months"]["10_month"][data['current_language']]),
                KeyboardButton(text=translations["months"]["11_month"][data['current_language']]),
                KeyboardButton(text=translations["months"]["12_month"][data['current_language']])
            ],
            [
                KeyboardButton(text=translations["months"]["back"][data['current_language']]),
                KeyboardButton(text=translations["months"]["back_to_main"][data['current_language']])
            ]
        ],
        resize_keyboard=True
    )