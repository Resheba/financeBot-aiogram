from aiogram import Router
from aiogram.filters import Command, CommandObject
import re
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from datetime import datetime, timedelta, timezone


from sheetAPI.base import DATE_FORMAT, OPERATIONS_TYPES
from sheetAPI.operation import create_operation, Operation
from states import OperationStateGroup
from keyboards import CompletedKeyboard, DeletedKeyboard, OperationCreditEditCallback, OperationCreditSelectCallback, OperationDirectionCallback, OperationDirectionEditCallback, OperationInOutComeCallback, OperationInOutComeEditCallback, OperationLasOKKeyboard, OperationStateNullEditCallback, OperationStateNullSelectCallback, OperationStateOneEditCallback, OperationStateOneSelectCallback, OperationStateTwoEditCallback, OperationStateTwoSelectCallback, buildDirectionsKeyboard, buildEditableDirectionsKeyboard, buildEditableInOutComeKeyboard, buildEditableOperationKeyboard, buildEditableStateNullKeyboard, buildEditableStateOneKeyboard, buildEditableStateTwoKeyboard, buildInOutComeKeyboard, buildStateNullKeyboard, buildStateOneKeyboard, buildStateTwoKeyboard, buildWalletsKeyboard


operation = Router()


@operation.message(Command(commands=['operation']))
async def operation_send_handler(message: Message, state: FSMContext, command: CommandObject):
    if command.args:
        args = [arg.strip() for arg in command.args.split(',', 1)]
        args_len = len(args)
        if args_len <= 2:
            sum = args[0]
            comment = args[1] if args_len > 1 else None
            try:
                sum = float(sum)
            except:
                await message.answer('<code>/operation {Сумма}, {Комментарий}</code>')
                return
            keyboard = await buildWalletsKeyboard(message.from_user.id)
            if keyboard:
                await message.answer('Выберите реквизит:', reply_markup=keyboard)
                await state.update_data(sum=sum, comment=comment)
                await state.set_state(OperationStateGroup.Wallet)
            else:
                await message.answer(text='На Вашем аккаунте отсутствуют кошельки.\nПодробнее /account')
        
    else:
        await message.answer('<code>/operation {Сумма}, {Комментарий}</code>')


@operation.message(lambda message: re.match(r'^\d', message.text))
async def operation_send_text_handler(message: Message, state: FSMContext):
    args = [arg.strip() for arg in message.text.split(',', 1)]
    args_len = len(args)
    if args_len <= 2:
        sum = args[0]
        comment = args[1] if args_len > 1 else None
        try:
            sum = float(sum)
        except:
            await message.answer('Введите сумму и коментарий через запятую')
            return
        keyboard = await buildWalletsKeyboard(message.from_user.id)
        if keyboard:
            await message.answer('Выберите реквизит:', reply_markup=keyboard)
            await state.update_data(sum=sum, comment=comment)
            await state.set_state(OperationStateGroup.Wallet)
        else:
            await message.answer(text='На Вашем аккаунте отсутствуют кошельки.\nПодробнее /account')
    else:
        await message.answer('Введите сумму и коментарий через запятую')


# WALLET CHOOSE


@operation.callback_query(OperationCreditSelectCallback.filter())
async def operation_wallet_handler(query: CallbackQuery, callback_data: OperationCreditSelectCallback, state: FSMContext):
    credit = callback_data.credit
    await state.update_data(credit=credit)
    
    await query.message.edit_reply_markup(reply_markup=await buildEditableOperationKeyboard(callback_data.pack(), first_edit=True))
    await state.set_state(OperationStateGroup.StateNull)

    keyboard = await buildStateNullKeyboard()
    if keyboard:
        await query.message.answer('Выберите статью 0 уровня:', reply_markup=keyboard)

@operation.callback_query(OperationCreditEditCallback.filter())
async def operation_wallet_edit_handler(query: CallbackQuery, callback_data: OperationCreditEditCallback, state: FSMContext):
    if callback_data.isKeyboardBuilder:
        keyboard = await buildWalletsKeyboard(user_id=query.from_user.id, editable=True)
        await query.message.edit_reply_markup(reply_markup=keyboard)
    else:
        await state.update_data(credit=callback_data.credit)
        keyboard = await buildEditableOperationKeyboard(callback_data.pack())
        await query.message.edit_reply_markup(reply_markup=keyboard)


# NULL STATE CHOOSE


@operation.callback_query(OperationStateNullSelectCallback.filter())
async def operation_state_null_handler(query: CallbackQuery, callback_data: OperationStateNullSelectCallback, state: FSMContext):
    
    keyboard, data = await buildEditableStateNullKeyboard(callback_data, first_edit=True)
    await query.message.edit_reply_markup(reply_markup=keyboard)
    
    await state.update_data(state0=data)

    state0 = OPERATIONS_TYPES.get(data)
    if state0:
        if len(state0) == 1:
            state1 = tuple(state0.keys())[0]
            await state.update_data(state1=state1)
            # Here state 1 editable
            keyboardOneState, _ = await buildEditableStateOneKeyboard(OperationStateOneEditCallback(state=hash(state1), isKeyboardBuilder=True), state0=data)
            await query.message.answer('Выберите статью 1 уровня:', reply_markup=keyboardOneState)

            values = tuple(state0.values())[0]
            if len(values) > 1:
                await state.set_state(OperationStateGroup.StateTwo)
                await query.message.answer('Выберите статью 2 уровня:', reply_markup=await buildStateTwoKeyboard(state0=data, state1=state1))
            elif len(values) == 1: 
                await state.update_data(state2=values[0])
                # Here state 2 editable
                keyboardTwoState, _ = await buildEditableStateTwoKeyboard(callback_data=OperationStateTwoEditCallback(state=hash(values[0]), isKeyboardBuilder=True), state0=data, state1=state1)
                await query.message.answer('Выберите статью 2 уровня:', reply_markup=keyboardTwoState)

                await state.set_state(OperationStateGroup.Direction)
                await query.message.answer('Выберите направление:', reply_markup=await buildDirectionsKeyboard())
            else:
                keyboardTwoState, _ = await buildEditableStateTwoKeyboard(callback_data=OperationStateTwoEditCallback(state='0', isKeyboardBuilder=True), state0=data, state1=state1)
                await query.message.answer('Выберите статью 2 уровня:', reply_markup=keyboardTwoState)

                await state.set_state(OperationStateGroup.Direction)
                await query.message.answer('Выберите направление:', reply_markup=await buildDirectionsKeyboard())
        elif len(state0) > 1:
            await state.set_state(OperationStateGroup.StateOne)
            await query.message.answer('Выберите статью 1 уровня:', reply_markup=await buildStateOneKeyboard(state0=data))
        else:
            await query.answer('Ошибка')

@operation.callback_query(OperationStateNullEditCallback.filter())
async def operation_state_null_edit_handler(query: CallbackQuery, callback_data: OperationStateNullEditCallback, state: FSMContext):
    if callback_data.isKeyboardBuilder:
        keyboard = await buildStateNullKeyboard(editable=True)
        await query.message.edit_reply_markup(reply_markup=keyboard)
    else:
        keyboard, data = await buildEditableStateNullKeyboard(callback_data)
        await state.update_data(state0=data)
        await query.message.edit_reply_markup(reply_markup=keyboard)


# ONE STATE CHOOSE


@operation.callback_query(OperationStateOneSelectCallback.filter())
async def operation_state_one_handler(query: CallbackQuery, callback_data: OperationStateOneSelectCallback, state: FSMContext):
    state_data = await state.get_data()
    state0 = state_data.get('state0')

    keyboard, data = await buildEditableStateOneKeyboard(callback_data=callback_data, state0=state0, first_edit=True)
    await query.message.edit_reply_markup(reply_markup=keyboard)

    await state.update_data(state1=data)

    state1 = OPERATIONS_TYPES.get(state0).get(data)
    if len(state1) == 0:
        keyboardTwoState, _ = await buildEditableStateTwoKeyboard(callback_data=OperationStateTwoEditCallback(state='0', isKeyboardBuilder=True), state0=state0, state1=data)
        await query.message.answer('Выберите статью 2 уровня:', reply_markup=keyboardTwoState)

        await state.set_state(OperationStateGroup.Direction)
        await query.message.answer('Выберите направление:', reply_markup=await buildDirectionsKeyboard())
    elif len(state1) == 1: 
        await state.update_data(state2=state1[0])

        keyboardTwoState, _ = await buildEditableStateTwoKeyboard(callback_data=OperationStateTwoEditCallback(state=state1[0], isKeyboardBuilder=True), state0=state0, state1=data)
        await query.message.answer('Выберите статью 2 уровня:', reply_markup=keyboardTwoState)

        await state.set_state(OperationStateGroup.Direction)
        await query.message.answer('Выберите направление:', reply_markup=await buildDirectionsKeyboard())
    elif len(state1) > 1:
        await state.set_state(OperationStateGroup.StateTwo)
        await query.message.answer('Выберите статью 2 уровня:', reply_markup=await buildStateTwoKeyboard(state0=state0, state1=data))


@operation.callback_query(OperationStateOneEditCallback.filter())
async def operation_state_one_edit_handler(query: CallbackQuery, callback_data: OperationStateOneEditCallback, state: FSMContext):
    state0 = (await state.get_data()).get('state0')
    if callback_data.isKeyboardBuilder:
        keyboard = await buildStateOneKeyboard(editable=True, state0=state0)
        await query.message.edit_reply_markup(reply_markup=keyboard)
    else:
        keyboard, data = await buildEditableStateOneKeyboard(callback_data, state0=state0)
        await state.update_data(state1=data)
        await query.message.edit_reply_markup(reply_markup=keyboard)
    

# TWO STATE CHOOSE


@operation.callback_query(OperationStateTwoSelectCallback.filter())
async def operation_state_two_handler(query: CallbackQuery, callback_data: OperationStateTwoSelectCallback, state: FSMContext):
    state_data = await state.get_data()
    state0 = state_data.get('state0')
    state1 = state_data.get('state1')

    keyboard, data = await buildEditableStateTwoKeyboard(callback_data=callback_data, state0=state0, state1=state1, first_edit=True)
    await query.message.edit_reply_markup(reply_markup=keyboard)

    await state.update_data(state2=data)

    await state.set_state(OperationStateGroup.Direction)
    await query.message.answer('Выберите направление:', reply_markup=await buildDirectionsKeyboard())

@operation.callback_query(OperationStateTwoEditCallback.filter())
async def operation_state_two_edit_handler(query: CallbackQuery, callback_data: OperationStateTwoEditCallback, state: FSMContext):
    data = await state.get_data()
    state0 = data.get('state0')
    state1 = data.get('state1')
    if callback_data.isKeyboardBuilder:
        keyboard = await buildStateTwoKeyboard(editable=True, state0=state0, state1=state1)
        if keyboard:
            await query.message.edit_reply_markup(reply_markup=keyboard)
        else:
            keyboardTwoState, _ = await buildEditableStateTwoKeyboard(callback_data=OperationStateTwoEditCallback(state='0', isKeyboardBuilder=True), state0=state0, state1=state1)
            await query.message.edit_reply_markup(reply_markup=keyboardTwoState)
            data.pop('state2')
            await state.set_data(data)
            await query.answer('Нет статей уровнем ниже!')
    else:
        keyboard, data = await buildEditableStateTwoKeyboard(callback_data, state0=state0, state1=state1)
        await state.update_data(state2=data)
        await query.message.edit_reply_markup(reply_markup=keyboard)


# DIRECTION CHOOSE


@operation.callback_query(OperationDirectionCallback.filter())
async def operation_direction_handler(query: CallbackQuery, callback_data: OperationDirectionCallback, state: FSMContext):
    await state.update_data(direction=callback_data.dir)

    await query.message.edit_reply_markup(reply_markup=await buildEditableDirectionsKeyboard(callback=callback_data, first_edit=True))
    
    await state.set_state(OperationStateGroup.Income)
    await query.message.answer('Выберите тип операции:', reply_markup=await buildInOutComeKeyboard())

@operation.callback_query(OperationDirectionEditCallback.filter())
async def operation_direction_edit_handler(query: CallbackQuery, callback_data: OperationDirectionEditCallback, state: FSMContext):
    if callback_data.isKeyboardBuilder:
        keyboard = await buildDirectionsKeyboard(editable=True)
        await query.message.edit_reply_markup(reply_markup=keyboard)
    else:
        keyboard = await buildEditableDirectionsKeyboard(callback_data)
        await state.update_data(direction=callback_data.dir)
        await query.message.edit_reply_markup(reply_markup=keyboard)


# IN/OUT COME CHOOSE


@operation.callback_query(OperationInOutComeCallback.filter())
async def operation_in_out_come_handler(query: CallbackQuery, callback_data: OperationInOutComeCallback, state: FSMContext):
    await state.update_data(income=callback_data.income)

    await query.message.edit_reply_markup(reply_markup=await buildEditableInOutComeKeyboard(callback=callback_data, first_edit=True))

    await query.message.answer('Отправить?', reply_markup=OperationLasOKKeyboard.keyboard)

@operation.callback_query(OperationInOutComeEditCallback.filter())
async def operation_direction_edit_handler(query: CallbackQuery, callback_data: OperationInOutComeEditCallback, state: FSMContext):
    if callback_data.isKeyboardBuilder:
        keyboard = await buildInOutComeKeyboard(editable=True)
        await query.message.edit_reply_markup(reply_markup=keyboard)
    else:
        keyboard = await buildEditableInOutComeKeyboard(callback_data)
        await state.update_data(income=callback_data.income)
        await query.message.edit_reply_markup(reply_markup=keyboard)


# CONFIRM


@operation.callback_query(lambda query: query.data in ('oper_ok', 'oper_no'))
async def last_check_handler(query: CallbackQuery, state: FSMContext):
    if query.data == 'oper_ok':
        data = await state.get_data()
        state_last = data.get('state2', data.get('state1', data.get('state0')))
        date = datetime.now(timezone(offset=timedelta(hours=5))).strftime(format=DATE_FORMAT)
        
        data.pop('state0', None)
        data.pop('state1', None)
        data.pop('state2', None)
        
        oper = Operation(user_id=query.from_user.id, username=query.from_user.username, date=date, state=state_last, **data)
        
        if await create_operation(oper):
            await query.answer(text='Упешно!')
            await query.message.edit_reply_markup(reply_markup=CompletedKeyboard.keyboard)
            await query.message.answer(text='Напишите сумму и комментарий')
        else:
            await query.answer('Что-то пошло не так...')
    else:
        await query.answer('Отмена!')
        await query.message.edit_reply_markup(reply_markup=DeletedKeyboard.keyboard)
        await query.message.answer(text='Напишите сумму и комментарий')
    await state.clear()


@operation.message()
async def operation_help_handler(message: Message):
    await message.answer('Введите сумму и коментарий через запятую')

