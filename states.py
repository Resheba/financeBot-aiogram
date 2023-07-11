from aiogram.fsm.state import State, StatesGroup


class RegistrationStateGrope(StatesGroup):
    Wallet = State()
    Confirm = State()


class OperationStateGroup(StatesGroup):
    Wallet = State()
    StateNull = State()
    StateOne = State()
    StateTwo = State()
    Direction = State()
    Income = State()