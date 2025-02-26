from aiogram.fsm.context import FSMContext
from aiogram import types, Bot

from user_side.functions.month_selection import choosing_month
from user_side.states.state import ProcessState
from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
import json
from user_side.functions.user_relation_to_baby import relationship_to_baby

# Sirojiddin Abduraxmonov
# Info : Viloyatlarni chiqarish uchun ishlatiladi.
async def user_get_region_answer(message:types.Message,state:FSMContext):
    await state.set_state(ProcessState.user_choose_district)
    await state.update_data(region=message.text)
    await message.answer("Endi tumanni tanlang",reply_markup = await get_district_btn(message.text))

# Sirojiddin Abduraxmonov
# Info : Tumanlarni chiqarish uchun ishlatiladi.
async def get_district_btn(region : str):
    with open("./user_side/data/regions.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    button = ReplyKeyboardBuilder()

    for value in data[region]:
        button.button(text = value)

    button.adjust(2)
    button.row(KeyboardButton(text = "🔙 Ortga"), KeyboardButton(text = "🏠 Bosh Sahifa"))
    return button.as_markup(resize_keyboard = True)

# Begzod Turdibekov
# Info : Testni qayta boshlash uchun ishlataman
async def try_pass_exam_again_answer(message : types.Message, state : FSMContext):
    await relationship_to_baby(message, state) # Testning boshlang'ich qiymatiga qaytadi.

# Begzod Turdibekov
# Info : Testni to'xtatish uchun ishlataman.
async def stop_test_action_answer(message: types.Message, bot : Bot, state : FSMContext):
    data = await state.get_data()
    if data.get('message'):
        message : types.Message = data['message'] # Eng ohirgi message yuklab qo'ygan man o'shani olayapma.

        await bot.delete_message(chat_id = message.chat.id, message_id=message.message_id) # eng ohirig habarni o'chirib yuborayapman.
        await choosing_month(message, state) # oylarni tanlash oynasini qayta chaqirayapman.
    else:
        print("message yo'q")

