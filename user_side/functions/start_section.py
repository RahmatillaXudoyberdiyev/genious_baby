from aiogram import Bot, types,F
from user_side import keyboard
from aiogram.fsm.context import FSMContext
from user_side.states.state import ProcessState

async def start_command_answer(message : types.Message, bot : Bot, state : FSMContext):
    await state.set_state(ProcessState.user_start_command)
    await message.answer(text = "Hush kelibsiz foydalanuvchi!", reply_markup=keyboard.languages)

async def language_command_answer(message : types.Message, bot : Bot, state : FSMContext):
    await state.set_state(ProcessState.user_language_chose_menu)
    await message.answer(text="MENU", reply_markup=keyboard.menu_buttons)