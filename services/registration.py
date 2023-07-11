from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery

from states import RegistrationStateGrope
from sheetAPI.user import USERS, User, edit_user_credits
from keyboards import RegistrationConfirmKeyboard, RegistrationConfirmCallback, RegistrationCreditsSkipCallback, DeletedKeyboard, RegistrationWalletKeyboard, CompletedKeyboard

registration = Router()


@registration.message(RegistrationStateGrope.Wallet)
async def wallet_state_handler(message: Message, state: FSMContext):
    text = message.text
    credits = {credit.strip() for credit in text.split(',')}
    
    await state.update_data(credits=credits)
    await state.set_state(RegistrationStateGrope.Confirm)
    await message.answer('Всё ли верно?\n\nВаши кошельки/карты выведены построчно:\n'+'\n'.join(credits), reply_markup=RegistrationConfirmKeyboard.keyboard)


@registration.callback_query(RegistrationConfirmCallback.filter())
async def wallet_callback_confirm(query: CallbackQuery, callback_data: RegistrationConfirmCallback, state: FSMContext):
    if callback_data.result:
        credits = (await state.get_data()).get('credits')
        await edit_user_credits(user_id=query.from_user.id, credits=credits)
        await state.clear()
        await query.message.edit_reply_markup(reply_markup=CompletedKeyboard.keyboard)
        
        await query.message.answer(text='Напишите сумму и комментарий')
    else:
        await query.message.answer('Впишите названия Ваших карт/кошельков. Кошельки/карты перечисляйте через запятые, не добавляйте комментариев и лишних символов.', reply_markup=RegistrationWalletKeyboard.keyboard)
        await state.set_state(RegistrationStateGrope.Wallet)
        await query.message.edit_reply_markup(reply_markup=DeletedKeyboard.keyboard)


@registration.callback_query(RegistrationCreditsSkipCallback.filter())
async def wallet_callback_skip(query: CallbackQuery, callback_data: RegistrationCreditsSkipCallback, state: FSMContext):
    await query.message.delete_reply_markup()
    if callback_data.skip:
        await state.clear()
        await query.answer('Ввод кошельков пропущен')
        await query.message.edit_reply_markup(reply_markup=DeletedKeyboard.keyboard)
