import json
from aiogram import types
from aiogram.fsm.context import FSMContext
from numpy.ma.core import resize

from user_side.keyboards.inline_keyboards import generate_options
from user_side.states.state import ProcessState
from user_side.keyboards.regions import user_ask_submit_answer_btn, stop_test_answer_btn
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "Testni to'xtatish")]
    ],
    resize_keyboard=True
)

# JSON ma’lumotlarini yuklash
with open("./user_side/data/questions_data.json", "r", encoding="utf-8") as file:
    quiz_data = json.load(file)

# JSON ma’lumotlarini yuklash
with open("./user_side/translations/result_regions_district.json", "r", encoding="utf-8") as file:
    translation_data = json.load(file)

async def start_quiz(message: types.Message, state: FSMContext):
    # await state.set_state(ProcessState.answering)

    data = await state.get_data()
    # score = data["score"]
    # chosen_month = data["chosen_month"]
    language: str = data.get("language")

    chosen_month = int(message.text.split()[0])
    print(chosen_month)
    await state.update_data(chosen_month = chosen_month, score=0, current_index=0)
    await message.answer("Test boshlandi 🚀.", reply_markup= await stop_test_answer_btn(translation_data, language, 'testing'))
    await send_question(message, state)


async def send_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    index = data["current_index"]
    chosen_month = data["chosen_month"]
    language = data['language']

    print(chosen_month)
    print(quiz_data)
    questions = quiz_data[chosen_month - 1]["questions"][:2]

    if index >= len(questions): 
        await show_result(message, state)
        return

    question_data = questions[index]
    question_text = question_data["question"][language]
    text = f"{question_text}\n(Выберите один ответ)"  

    buttons = generate_options(question_data["id"], question_data["answers"], language)
    await state.update_data(message = message)

    # Bu bilan men yangi jo'natilayotgan habarni tutib olayapman
    send_message =await message.answer(text, reply_markup=buttons)
    await state.update_data(message=send_message) # Bu yerda yangi olingan habarni saqlab qo'ymoqdaman.

async def check_answer(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data["current_index"]
    score = data["score"]
    chosen_month = data["chosen_month"]
    language = data.get("language")

    question_key, option_key, point = call.data.split(":")
    score += int(point)

    await state.update_data(score=score, current_index=index + 1)
    await call.message.delete()
    await send_question(call.message, state)



async def show_result(message: types.Message, state: FSMContext):
    # await state.set_state(ProcessState.user_choose_region)
    data = await state.get_data()
    score = data["score"]
    chosen_month = data["chosen_month"]
    language : str = data.get("language")

    evaluations = quiz_data[chosen_month]["evaluation"]

    result_text = None
    for eval_range in evaluations:
        min_score = eval_range["min_score"]
        max_score = eval_range["max_score"]
        if min_score <= score <= max_score:
            result_text = eval_range["result"][language.lower()]
            break

    if not result_text:  
        result_text = "Natija topilmadi / Result not found / Результат не найден"

    await message.answer(f"Test yakunlandi!\nJami ball: {score}\n\nNatija: {result_text}", reply_markup=user_ask_submit_answer_btn(translation_data,language, 'save_result'))
