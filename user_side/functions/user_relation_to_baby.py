from aiogram import Bot, types

from user_side.functions.month_selection import choosing_month
from user_side.keyboards.keyboard import get_relationship_keyboard
from aiogram.fsm.context import FSMContext
from user_side.states.state import ProcessState
from user_side.translations.translation import translate_into


# Rahmatilla Xudoyberdiyev
async def relationship_to_baby(message : types.Message, state : FSMContext):

    try:
        path = "user_side/translations/relation_to_baby.json"
        data = await state.get_data()

        question_text = translate_into(path, data, "relation_to_baby_label")


        await message.answer(text=question_text, reply_markup=get_relationship_keyboard(data))
        await state.set_state(ProcessState.user_relation_to_baby)

    except Exception as e:
        print(e)