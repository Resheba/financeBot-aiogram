from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from sheetAPI.user import get_user_by_id
from sheetAPI.base import BUTTONS_IN_OUT, DIRECTIONS_TYPES, OPERATIONS_TYPES

class RegistrationConfirmCallback(CallbackData, prefix='reg_confirm'):
    result: bool

class RegistrationCreditsSkipCallback(CallbackData, prefix='skip'):
    skip: bool


class RegistrationWalletKeyboard:
    button_skip = InlineKeyboardButton(text='Пропустить', callback_data='skip:True')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_skip]])

class RegistrationConfirmKeyboard:
    button_ok = InlineKeyboardButton(text='Верно', callback_data='reg_confirm:True')
    button_bad = InlineKeyboardButton(text='Ошибка', callback_data='reg_confirm:False')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_ok, button_bad]], row_width=2)


class DeletedKeyboard:
    button_delete = InlineKeyboardButton(text='❌', callback_data='helper')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_delete]])

class CompletedKeyboard:
    bitton_complete = InlineKeyboardButton(text='✅', callback_data='helper')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[bitton_complete]])



class AccountMenuKeyboard:
    button_edit_credits = InlineKeyboardButton(text='Изменить кошельки', callback_data='reg_confirm:False')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_edit_credits]])


async def buildEditableOperationKeyboard(callback_data: str, first_edit: bool = False):
    data = callback_data.split(':')
    answer = data[1] + '✅'
    answer_button = InlineKeyboardButton(text=answer, callback_data='pass')
    button_edit = InlineKeyboardButton(text='Изменить', callback_data=f'{data[0]}{"_edit" if first_edit else ""}:{data[1]}:True')
    return InlineKeyboardMarkup(inline_keyboard=[[answer_button],[button_edit]])


class OperationCreditSelectCallback(CallbackData, prefix='oper_credit'):
    credit: str
    passed: bool

class OperationCreditEditCallback(CallbackData, prefix='oper_credit_edit'):
    credit: str
    isKeyboardBuilder: bool

async def buildWalletsKeyboard(user_id: int|str, editable: bool = False):
    user = await get_user_by_id(user_id)
    if user:
        credits = user.credits
        if credits:
            buttons = [[InlineKeyboardButton(text=credit, callback_data=f'oper_credit{"_edit" if editable else ""}:{credit}:False')] for credit in credits]
            return InlineKeyboardMarkup(inline_keyboard=buttons)
        else:
            return None
        



class OperationStateNullSelectCallback(CallbackData, prefix='oper_state'):
    state: str
    passed: bool

class OperationStateNullEditCallback(CallbackData, prefix='oper_state_edit'):
    state: str
    isKeyboardBuilder: bool

async def buildStateNullKeyboard(editable: bool = False):
    if OPERATIONS_TYPES:
        keys = OPERATIONS_TYPES.keys()
        buttons = [[InlineKeyboardButton(text=key, callback_data=f'oper_state{"_edit" if editable else ""}:{hash(key)}:False')] for key in keys]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    else:
        return None

async def buildEditableStateNullKeyboard(callback_data: OperationStateNullEditCallback, first_edit: bool = False):
    data_hash = callback_data.state
    for key in OPERATIONS_TYPES.keys():
        if hash(key) == int(data_hash):
            data = key
            break
    answer = data + '✅'
    answer_button = InlineKeyboardButton(text=answer, callback_data='pass')
    button_edit = InlineKeyboardButton(text='Изменить', callback_data=f'{callback_data.__prefix__}{"_edit" if first_edit else ""}:{data_hash}:True')
    return InlineKeyboardMarkup(inline_keyboard=[[answer_button],[button_edit]]), data



class OperationStateOneSelectCallback(CallbackData, prefix='oper_state1'):
    state: str
    passed: bool

class OperationStateOneEditCallback(CallbackData, prefix='oper_state1_edit'):
    state: str
    isKeyboardBuilder: bool

async def buildStateOneKeyboard(state0: str, editable: bool = False):
    state1 = OPERATIONS_TYPES.get(state0)
    if state1:
        keys = state1.keys()
        buttons = [[InlineKeyboardButton(text=key, callback_data=f'oper_state1{"_edit" if editable else ""}:{hash(key)}:False')] for key in keys]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    else:
        return None

async def buildEditableStateOneKeyboard(callback_data: OperationStateOneEditCallback, state0: str, first_edit: bool = False):
    data_hash = callback_data.state
    data = '-'
    for key in OPERATIONS_TYPES.get(state0).keys():
        if hash(key) == int(data_hash):
            data = key
            break
    answer = data + '✅'
    answer_button = InlineKeyboardButton(text=answer, callback_data='pass')
    button_edit = InlineKeyboardButton(text='Изменить', callback_data=f'{callback_data.__prefix__}{"_edit" if first_edit else ""}:{data_hash}:True')
    
    return InlineKeyboardMarkup(inline_keyboard=[[answer_button],[button_edit]]), data



class OperationStateTwoSelectCallback(CallbackData, prefix='oper_state2'):
    state: str
    passed: bool

class OperationStateTwoEditCallback(CallbackData, prefix='oper_state2_edit'):
    state: str
    isKeyboardBuilder: bool

async def buildStateTwoKeyboard(state0: str, state1: str, editable: bool = False):
    state2 = OPERATIONS_TYPES.get(state0).get(state1)
    if state2:
        keys = state2
        buttons = [[InlineKeyboardButton(text=key, callback_data=f'oper_state2{"_edit" if editable else ""}:{hash(key)}:False')] for key in keys]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    else:
        return None

async def buildEditableStateTwoKeyboard(callback_data: OperationStateTwoEditCallback, state0: str, state1: str, first_edit: bool = False):
    data_hash = callback_data.state
    data = '-'
    for key in OPERATIONS_TYPES.get(state0).get(state1):
        if hash(key) == int(data_hash):
            data = key
            break
    answer = data + '✅'
    answer_button = InlineKeyboardButton(text=answer, callback_data='pass')
    button_edit = InlineKeyboardButton(text='Изменить', callback_data=f'{callback_data.__prefix__}{"_edit" if first_edit else ""}:{data_hash}:True')
    
    return InlineKeyboardMarkup(inline_keyboard=[[answer_button],[button_edit]]), data



class OperationDirectionCallback(CallbackData, prefix='oper_dir'):
    dir: str
    passed: bool

class OperationDirectionEditCallback(CallbackData, prefix='oper_dir_edit'):
    dir: str
    isKeyboardBuilder: bool

async def buildDirectionsKeyboard(editable: bool = False):
    buttons = [[InlineKeyboardButton(text=direction, callback_data=f'oper_dir{"_edit" if editable else ""}:{direction}:False')] for direction in DIRECTIONS_TYPES]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def buildEditableDirectionsKeyboard(callback: OperationDirectionCallback, first_edit: bool = False):
    answer = callback.dir + '✅'
    answer_button = InlineKeyboardButton(text=answer, callback_data='pass')
    button_edit = InlineKeyboardButton(text='Изменить', callback_data=f'{callback.__prefix__}{"_edit" if first_edit else ""}:{callback.dir}:True')

    return InlineKeyboardMarkup(inline_keyboard=[[answer_button],[button_edit]])



class OperationInOutComeCallback(CallbackData, prefix='oper_in_out'):
    income: str
    passed: bool

class OperationInOutComeEditCallback(CallbackData, prefix='oper_in_out_edit'):
    income: str
    isKeyboardBuilder: bool

async def buildInOutComeKeyboard(editable: bool = False):
    buttons = [[InlineKeyboardButton(text=text, callback_data=f'oper_in_out{"_edit" if editable else ""}:{text}:False') for text in BUTTONS_IN_OUT]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def buildEditableInOutComeKeyboard(callback: OperationInOutComeCallback, first_edit: bool = False):
    answer = callback.income + '✅'
    answer_button = InlineKeyboardButton(text=answer, callback_data='pass')
    button_edit = InlineKeyboardButton(text='Изменить', callback_data=f'{callback.__prefix__}{"_edit" if first_edit else ""}:{callback.income}:True')

    return InlineKeyboardMarkup(inline_keyboard=[[answer_button],[button_edit]])


class OperationLasOKKeyboard:
    ok_button = InlineKeyboardButton(text='Отправить', callback_data='oper_ok')
    no_button = InlineKeyboardButton(text='Отменить', callback_data='oper_no')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[ok_button, no_button]])