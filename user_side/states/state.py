from aiogram.fsm.state import StatesGroup, State

class ProcessState(StatesGroup):
    user_start_command = State()
    user_language_chose_menu = State()