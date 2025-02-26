from aiogram import Bot, types
from user_side.keyboards.keyboard import get_languages_keyboard, get_menu_keyboard
from aiogram.fsm.context import FSMContext
from user_side.states.state import ProcessState

# Aydos Bekbergenov
async def start_command_answer(message : types.Message, state : FSMContext):
    await state.clear()
    await message.answer(text = "Xush kelibsiz foydalanuvchi!", reply_markup=get_languages_keyboard())
    await state.set_state(ProcessState.user_start_command)

async def language_command_answer(message : types.Message, state : FSMContext):
    data1 = await state.get_data()



    if message.text == '🇷🇺 Ru':
        language = 'russian'
        await state.update_data(language=message.text[3:].lower())
    elif message.text == '🇺🇸 En':
        language = 'english'
        await state.update_data(language=message.text[3:].lower())
    elif message.text == '🇺🇿 Uz':
        await state.update_data(language = message.text[3:].lower())
        language = 'uzbek'
    else:
        if curr_language:=data1.get("current_language"): language = curr_language 
        else: language = 'uzbek'

    await state.update_data(current_language = language)

    data2 = await state.get_data()
    

    await message.answer(text="Menu", reply_markup=get_menu_keyboard(data2))
    await state.set_state(ProcessState.user_language_chose_menu)
