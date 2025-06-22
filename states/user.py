from aiogram.fsm.state import StatesGroup, State


class AddDailyTask(StatesGroup):
    waiting_for_task_text = State()
    waiting_for_accept = State()
