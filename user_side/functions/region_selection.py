from logging import exception

from aiogram.fsm.context import FSMContext
from aiogram import types, Bot

from user_side.functions.month_selection import choosing_month
from user_side.functions.start_section import language_command_answer
from user_side.states.state import ProcessState
from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder
import json
from user_side.functions.user_relation_to_baby import relationship_to_baby
from user_side.data.users import ids
from user_side.keyboards.regions import get_regions, user_ask_submit_answer_btn
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",  # Agar MySQL serveri boshqa joyda bo'lsa, IP yoki domenni kiriting
    user="root",       # MySQL foydalanuvchi nomi
    password="begzod",  # MySQL paroli
    database="genius_baby"  # Bazaning nomi
)


# Begzod Turdibekov
# Info : viloyat va tumanlar json fayli
with open("./user_side/data/regions.json", "r", encoding="utf-8") as file:
    region_district = json.load(file)

# Begzod Turdibekov
# Info : Tarjimalar
with open("./user_side/translations/result_regions_district.json", "r", encoding="utf-8") as file:
    translation_data = json.load(file)

# Sirojiddin Abduraxmonov
# Info : Viloyatlarni chiqarish uchun ishlatiladi.
async def user_get_district_answer(message:types.Message,state:FSMContext):

    data = await state.get_data()
    lang = data['language']
    region = message.text
    if data.get('region'):
        region = data['region']
    if region in region_district:
        await state.set_state(ProcessState.user_choose_district)
        await state.update_data(region=region)
        await message.answer(translation_data['choosing_region']['select_district'][lang],reply_markup = await get_district_btn(region, data['language']))
    else:
        await message.answer("Kiritilayotgan qiymat viloyatlar ichida yo'q!")

# Sirojiddin Abduraxmonov
# Info : Tumanlarni chiqarish uchun ishlatiladi.
async def get_district_btn(region : str, lang):

    button = ReplyKeyboardBuilder()

    for value in region_district[region]:
        button.button(text = value)

    button.adjust(2)
    button.row(KeyboardButton(text = translation_data['save_result']['back'][lang]),KeyboardButton(text = translation_data['save_result']['back_to_main'][lang]))
    return button.as_markup(resize_keyboard = True)

# Begzod Turdibekov
# Info : Orqaga qaytish uchun
async def go_back_function_answer(message : types.Message, state : FSMContext):
    data = await state.get_data()
    current = await state.get_state()
    if current == ProcessState.user_choose_district:
        await state.set_state(ProcessState.user_choose_region)
        await state.update_data(region = None)
        await message.answer(translation_data['choosing_region']['select_region'][data['language']], reply_markup= await get_regions(translation_data, data['language']))
    if current == ProcessState.user_save_result_menu:
        await state.update_data(district = None)
        await user_get_district_answer(message, state)


# Begzod turdibekov
# Info : Natijani saqlash so'rash
async def ask_save_result_answer(message : types.Message, state : FSMContext):
    await state.set_state(ProcessState.user_save_result_menu)
    data = await state.get_data()
    for value in region_district.values():
        if message.text in value:
            ids[message.from_user.id] = {"score": ['score'], "result": data['result']}
            await state.update_data(district=message.text)
            data = await state.get_data()
            await message.answer("Natijani saqlaysizmi ? / Qayta test ishlaysizmi ?", reply_markup=user_ask_submit_answer_btn(translation_data,data['language'], 'save_result'))
            break
    else:
        await message.answer("Tumanlardan birini tanlang!")
# Begzod Turdibekov
# Info : Natijani saqlashim kerak bo'ladi. Agarda barcha amallar to'g'ri bajarilgan bo'lsa

async def confirm_action_answer(message : types.Message, state : FSMContext):
    data = await state.get_data()

    try :
        query = conn.cursor()
        query.execute("select regions.id, district.id from regions "
                      "join district on district.region_id = regions.id "
                      "where regions.name = %s and district.name = %s", params=(data['region'], data['district']))
        result = query.fetchall()
        print(result)
        region_id = result[0][0]
        print("Ishladi.")
        district_id = result[0][1]
        print("Ishladi.")
        status_id = 1
        if data['relation'] == "Ona":
            status_id = 2
        elif data['relation'] == 'Ota':
            status_id = 1
        else:
            status_id = 3
        month = data['chosen_month']
        query.execute("Select month from history where telegram_id = %s" , (message.from_user.id,))
        result = query.fetchall()
        print(result)
        for value in result:
            if value[0] == month:
                query.execute("update history set score = %s, time = now(), status_id = %s, answer = %s, district_id = %s, region_id = %s where telegram_id = %s and month = %s", (data['score'], status_id, data['result'], district_id, region_id, message.from_user.id, month))
                conn.commit()
                print("Yangilandi.")
                break
        else:
            query.execute(
                "Insert into history(score, month, answer, time, status_id, telegram_id, district_id,region_id) values"
                "(%s, %s, %s, now(), %s, %s, %s, %s)",
                params=(data['score'], data['chosen_month'], data['result'], status_id, data['telegram_id'], district_id, region_id))
            conn.commit()
            print("Qo'shildi.")
        await message.answer(translation_data['testing']['result_info'][data['language']])
        await language_command_answer(message, state)
    except Exception as ex:
        print(ex)
        print("Xatolik bo'ldi.")



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

