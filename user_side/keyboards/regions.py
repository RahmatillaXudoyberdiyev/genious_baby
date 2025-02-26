from email.headerregistry import MessageIDHeader

from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
import json
with open("./user_side/data/regions.json", "r", encoding="utf-8") as file:
    data = json.load(file)

async def get_regions():
    buttons = ReplyKeyboardBuilder()
    for region in data.keys():
        buttons.button(text = region)
    buttons.adjust(2)

    buttons.row(KeyboardButton(text = "🔙 Ortga"), KeyboardButton(text = "🏠 Bosh Sahifa"))

    buttons = buttons.as_markup()
    buttons.resize_keyboard = True

    return buttons



def user_ask_submit_answer_btn(data,lang, section):
    buttons = ReplyKeyboardBuilder()

    buttons.row(KeyboardButton(text = data[section]['confirm'][lang]), KeyboardButton(text = data[section]['retake_test'][lang]))
    buttons.row(KeyboardButton(text=data[section]['back_to_main'][lang]))
    buttons = buttons.as_markup()
    buttons.resize_keyboard = True
    return buttons

async def stop_test_answer_btn(data, lang, section):
    buttons = ReplyKeyboardBuilder()
    buttons.button(text = data[section]['stop_test'][lang])

    return buttons.as_markup(resize_keyboard = True)

