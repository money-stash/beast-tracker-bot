from aiogram.fsm.state import StatesGroup, State


class ChangeGroup(StatesGroup):
    new_group_id = State()
