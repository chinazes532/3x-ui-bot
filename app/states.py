from aiogram.fsm.state import State, StatesGroup


class AddAdmin(StatesGroup):
    tg_id = State()


class SendAll(StatesGroup):
    text = State()


class AddTariff(StatesGroup):
    title = State()
    price = State()
    month_count = State()


class EditTariff(StatesGroup):
    new_title = State()
    new_price = State()
    new_month_count = State()