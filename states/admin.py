from aiogram.fsm.state import StatesGroup, State


class ChangeGroup(StatesGroup):
    new_group_id = State()


class FindUserMem(StatesGroup):
    user_identy = State()


# partner rotation frequency
class RotFreq(StatesGroup):
    new_freq = State()


class SendDmAdmin(StatesGroup):
    user_identy = State()
    message_text = State()


class NewChallenge(StatesGroup):
    name = State()
    duration = State()
    rules = State()
    action = State()
    accept = State()
