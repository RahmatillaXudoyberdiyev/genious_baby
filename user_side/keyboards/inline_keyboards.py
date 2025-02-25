from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_options(question_id, answers, language):
    buttons = []
    for answer_key, answer_data in answers.items():
        text = answer_data[language]
        callback_data = f"{question_id}:{answer_key}:{answer_data['score']}"
        buttons.append(InlineKeyboardButton(text=text, callback_data=callback_data))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
