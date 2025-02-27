from aiogram import Bot, types
from user_side.keyboards.keyboard import get_languages_keyboard, get_menu_keyboard
from aiogram.fsm.context import FSMContext
from user_side.states.state import ProcessState
import mysql.connector
from deep_translator import GoogleTranslator

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "begzod",
    "database": "genius_baby",
}


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

    await state.update_data(current_language = language, telegram_id = message.from_user.id)

    data2 = await state.get_data()
    

    await message.answer(text="Menu", reply_markup=get_menu_keyboard(data2))
    await state.set_state(ProcessState.user_language_chose_menu)


# Begzod Turdibekov
# Info : Tarixni ko'rsatish uchun

async def user_history_answer(message : types.Message, state : FSMContext):
    data = await state.get_data()
    conn = mysql.connector.connect(**db_config)
    query = conn.cursor()
    conn.query_attrs_clear()
    query.execute("Select status.name as status, history.time as vaqt, history.answer as result, history.month, district.name, regions.name, history.score from history "
                  "join status on status.id = history.status_id "
                  "join district on district.id = history.district_id "
                  "join regions on regions.id = history.region_id "
                  "where history.telegram_id = %s", (message.from_user.id,))
    result = query.fetchall()

    if len(result) == 0:
        await message.answer("Siz haqingizda ma'lumotlar topilmadi!")
    else:
        translator = GoogleTranslator(source='uz', target=data['language'])
        result.sort(key = lambda a : a[3])
        for value in result:
            info = (f"Test oluvchi : {value[0]}\n"
             f"Oy : {value[3]}\n"
             f"Ball : {value[6]}\n"
             f"Test Natija : {value[2]}\n"
             f"Yashash manzil : {value[5]} / {value[4]}\n"
             f"Vaqt : {value[1]}")
            await message.answer(translator.translate(info))
        conn.close()
