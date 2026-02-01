from aiogram.fsm.state import State, StatesGroup


class Administration(StatesGroup):

    report_data = State()
    old_monthly_finish_data = State()

