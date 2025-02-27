from aiogram import Bot, types
from user_side.keyboards.keyboard import get_months_keyboard, get_relationship_keyboard
from aiogram.fsm.context import FSMContext
from user_side.states.state import ProcessState
from user_side.translations.translation import translate_into
import json
RELATIONSHIP_OPTIONS = {
    "Otasi", "Father", "Отец",          
    "Onasi", "Mother", "Мать",         
    "Boshqa", "Other", "Другое"        
}

with open("./user_side/translations/keyboard_translations.json", "r", encoding="utf-8") as file:
    translation_data = json.load(file)

# Rahmatilla Xudoyberdiyev
async def choosing_month(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        path = "user_side/translations/month_selection.json"
        relation_text = message.text
        if data.get("user_relation_to_baby"):
            relation_text = data['user_relation_to_baby']
        if relation_text in RELATIONSHIP_OPTIONS:
            relation = ""
            if relation_text in ["Otasi", "Father", "Отец"]:
                relation = "Ota"
            elif relation_text == ["Onasi", "Mother", "Мать"]:
                relation = "Ona"
            else:
                relation = "Boshqa"
            await state.update_data(user_relation_to_baby=relation_text, relation = relation)
            prompt_text = translate_into(path, data, "choose_month_prompt")
            await message.answer(
                text=prompt_text,
                reply_markup=get_months_keyboard(data)
            )
            await state.set_state(ProcessState.user_choose_month)
        else:
            print("Xato")
            error_text = translate_into(path, data, "invalid_choice_error")
            await message.answer(
                text=error_text,
                reply_markup=get_relationship_keyboard(data)
            )
            # await state.set_state(ProcessState.user_relation_to_baby)

    except Exception as e:
        print(e)
