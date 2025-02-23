from aiogram import Bot, types
from user_side.keyboards.keyboard import get_months_keyboard
from aiogram.fsm.context import FSMContext
from user_side.states.state import ProcessState
from user_side.translations.translation import translate_into

RELATIONSHIP_OPTIONS = {
    "Otasi", "Father", "Отец",          
    "Onasi", "Mother", "Мать",         
    "Boshqa", "Other", "Другое"        
}

# Rahmatilla Xudoyberdiyev
async def choosing_month(message: types.Message, bot: Bot, state: FSMContext):
    try:
        data = await state.get_data()
        path = "user_side/translations/month_selection.json"

        if message.text in RELATIONSHIP_OPTIONS:
            await state.update_data(user_relation_to_baby=message.text)
            prompt_text = translate_into(path, data, "choose_month_prompt")
            await message.answer(
                text=prompt_text,
                reply_markup=get_months_keyboard(data)
            )
            await state.set_state(ProcessState.user_choose_month)
        else:
            error_text = translate_into(path, data, "invalid_choice_error")
            await message.answer(
                text=error_text,
                reply_markup=get_relationship_keyboard(data)
            )
            await state.set_state(ProcessState.user_relation_to_baby)

    except Exception as e:
        print(e)
