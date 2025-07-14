from aiogram.fsm.state import StatesGroup, State

class EditCar(StatesGroup):
    check = State()

class CreateApp(StatesGroup):
    start = State()
    choose_car = State()
    connect_apply = State()
    phone_apply = State()
    edit_phone = State()
    app_req = State()

class AddCar(StatesGroup):
    brand = State()
    model = State()
    number = State()
    year = State()

class ClientAuth(StatesGroup):
    waiting_phone = State()