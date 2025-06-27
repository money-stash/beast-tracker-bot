from aiogram.fsm.state import StatesGroup, State


class ChangeGroup(StatesGroup):
    new_group_id = State()


class FindUserMem(StatesGroup):
    user_identy = State()


class BanUser(StatesGroup):
    user_identy = State()
