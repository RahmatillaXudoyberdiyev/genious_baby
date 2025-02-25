from aiogram import Bot, types
from user_side.keyboards.keyboard import get_languages_keyboard, get_menu_keyboard
from aiogram.fsm.context import FSMContext
from user_side.states.state import ProcessState

# Aydos Bekbergenov
async def start_command_answer(message : types.Message, bot : Bot, state : FSMContext):
    await message.answer(text = "Xush kelibsiz foydalanuvchi!", reply_markup=get_languages_keyboard())
    await state.set_state(ProcessState.user_start_command)

async def language_command_answer(message : types.Message, bot : Bot, state : FSMContext):
    data1 = await state.get_data()

    await state.update_data(language = message.text[3:].lower())
    if message.text == '🇷🇺 Ru': language = 'russian'
    elif message.text == '🇺🇸 En': language = 'english'
    elif message.text == '🇺🇿 Uz': language = 'uzbek'
    else:
        if curr_language:=data1.get("current_language"): language = curr_language 
        else: language = 'uzbek'

    await state.update_data(current_language = language)

    data2 = await state.get_data()
    

    await message.answer(text="Menu", reply_markup=get_menu_keyboard(data2))
    await state.set_state(ProcessState.user_language_chose_menu)
