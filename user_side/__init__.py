from aiogram import Router, F
from aiogram.filters import Command
from user_side.functions.start_section import start_command_answer, language_command_answer
from config import ADMIN_IDS
from user_side.keyboard import menu_buttons
from user_side.states.state import ProcessState
from aiogram import F
router = Router()


router.message.register(start_command_answer, Command('start'), ~F.from_user.id.in_(ADMIN_IDS))
router.message.register(language_command_answer, ProcessState.user_start_command)

