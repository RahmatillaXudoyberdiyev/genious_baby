from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_options(question_id, answers, language):
    # buttons = []
    # for answer_key, answer_data in answers.items():
    #     text = answer_data[language]
    #     callback_data = f"{question_id}:{answer_key}:{answer_data['score']}"
    #
    #
    #     buttons.append(InlineKeyboardButton(text=text, callback_data=callback_data))
    keyboard = [[InlineKeyboardButton(text = answer_data[language], callback_data=f"{question_id}:{answer_key}:{answer_data['score']}")] for answer_key, answer_data in answers.items()]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# buttons = ["Tugma 1", "Tugma 2", "Tugma 3", "Tugma 4"]
# keyboard = [[InlineKeyboardButton(text, callback_data=text)] for text in buttons]