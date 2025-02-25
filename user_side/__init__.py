from aiogram import Router
from aiogram.filters import Command
from user_side.functions.start_section import start_command_answer, language_command_answer
from user_side.functions.user_relation_to_baby import relationship_to_baby
from user_side.functions.month_selection import choosing_month
from user_side.functions.quiz_section import start_quiz, check_answer
from config import ADMIN_IDS
from user_side.states.state import ProcessState
from aiogram import F
from operator import or_
router = Router()


START_TEST_VARIANTS = {"Testni Boshlash", "Start Test", "Начать тест"}
BACK_TO_MAIN_VARIANTS = {"Bosh sahifaga qaytish", "Back to Main", "Вернуться на главную"}
BACK_VARIANTS = {"Ortga", "Back", "Назад"}
MONTH_VARIANTS_POSTFIX = {"oylik", "months", "месяцев"}
MONTH_VARIANTS = set()
for variant in MONTH_VARIANTS_POSTFIX:
	for i in range(1, 13):
		MONTH_VARIANTS.add(f"{i} {variant}")

router.message.register(start_command_answer, Command('start'), ~F.from_user.id.in_(ADMIN_IDS))
router.message.register(start_command_answer, Command('lang'), ~F.from_user.id.in_(ADMIN_IDS))
router.message.register(language_command_answer, ProcessState.user_start_command)
router.message.register(relationship_to_baby, F.text.in_(START_TEST_VARIANTS), ProcessState.user_language_chose_menu)
router.message.register(language_command_answer, F.text.in_(BACK_TO_MAIN_VARIANTS), ProcessState.user_relation_to_baby)
router.message.register(choosing_month, ProcessState.user_relation_to_baby)
router.message.register(relationship_to_baby, F.text.in_(BACK_VARIANTS), ProcessState.user_choose_month)
router.message.register(language_command_answer, F.text.in_(BACK_TO_MAIN_VARIANTS), ProcessState.user_choose_month)
router.message.register(start_quiz, F.text.in_(MONTH_VARIANTS), ProcessState.user_choose_month)
router.callback_query.register(check_answer, ProcessState.user_choose_month)