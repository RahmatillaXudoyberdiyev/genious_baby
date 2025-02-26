from aiogram import Router
from aiogram.filters import Command

from user_side.functions.region_selection import user_get_region_answer, try_pass_exam_again_answer, \
	stop_test_action_answer
from user_side.functions.start_section import start_command_answer, language_command_answer
from user_side.functions.user_relation_to_baby import relationship_to_baby
from user_side.functions.month_selection import choosing_month
from user_side.functions.quiz_section import start_quiz, check_answer
from config import ADMIN_IDS
from user_side.states.state import ProcessState
from aiogram import F
router = Router()


START_TEST_VARIANTS = {"🎯 Testni Boshlash", "🎯 Start Test", "🎯 Начать тест"}
BACK_TO_MAIN_VARIANTS = {"🏠 Bosh Sahifa", "🏠 Main Page", "🏠 Домашняя Страница"}
BACK_VARIANTS = {"🔙 Ortga", "🔙 Back", "🔙 Назад"}
MONTH_VARIANTS_POSTFIX = {"oylik", "months", "month", "месяцев", "месяца", "месяц"}
RETAKE_THE_TEST_VARIANTS = {"🔁 Testni qayta ishlash", "🔁 Retake the test", "🔁 Пересдать тест"}
CONFIRM_VARIANTS = {"✅ Tasdiqlash", "✅ Confirm", "✅ Подтвердить"}
STOP_TEST_VARIANTS = {
     "🛑 Testni to'xtatish!",
      "🛑 Stop Test!",
      "🛑 Остановить Тест!"
    }

MONTH_VARIANTS = set()
for variant in MONTH_VARIANTS_POSTFIX:
	for i in range(1, 13):
		MONTH_VARIANTS.add(f"{i} {variant}")

router.message.register(start_command_answer, Command('start'), ~F.from_user.id.in_(ADMIN_IDS))
router.message.register(start_command_answer, Command('lang'), ~F.from_user.id.in_(ADMIN_IDS))
router.message.register(language_command_answer, F.text.in_(BACK_TO_MAIN_VARIANTS))
router.message.register(language_command_answer, ProcessState.user_start_command)
router.message.register(relationship_to_baby, F.text.in_(START_TEST_VARIANTS), ProcessState.user_language_chose_menu)
router.message.register(choosing_month, ProcessState.user_relation_to_baby)
router.message.register(relationship_to_baby, F.text.in_(BACK_VARIANTS), ProcessState.user_choose_month)
router.message.register(start_quiz, F.text.in_(MONTH_VARIANTS), ProcessState.user_choose_month)

router.message.register(stop_test_action_answer, ProcessState.user_choose_month, F.text.in_(STOP_TEST_VARIANTS))
router.callback_query.register(check_answer, ProcessState.user_choose_month)
# router.message.register(user_get_region_answer, ProcessState.user_choose_region)
router.message.register(try_pass_exam_again_answer, ProcessState.user_choose_month, F.text.in_(RETAKE_THE_TEST_VARIANTS))
