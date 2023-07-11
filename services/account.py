from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import AccountMenuKeyboard
from sheetAPI.user import get_user_by_id

account = Router()


@account.message(Command(commands=['account']))
async def account_menu_handler(message: Message):
    user = await get_user_by_id(message.from_user.id)
    if user:
        reg_date = user.reg_date
        credits = user.credits
        credits_str = ', '.join(credits) if credits else 'Пусто'
        await message.answer(f'Ваш Аккаунт, {message.from_user.first_name}\n\nДата регистрации: {reg_date}\nКошельки: {credits_str}', reply_markup=AccountMenuKeyboard.keyboard)
