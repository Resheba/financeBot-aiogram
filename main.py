import os, dotenv, logging, asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta, timezone

from sheetAPI.user import get_user_by_id, create_user, User
from sheetAPI.base import DATE_FORMAT
from states import RegistrationStateGrope
from keyboards import RegistrationWalletKeyboard

dotenv.load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')

main_router = Router()


@main_router.message(Command(commands=['start']))
async def command_start_handler(message: Message, state: FSMContext):
    user = await get_user_by_id(message.from_user.id)
    if user:
        await message.answer('Введите сумму и комментарий через запятую')
    else:
        user = User(user_id=message.from_user.id, username=message.from_user.username, reg_date=datetime.now(timezone(offset=timedelta(hours=5))).strftime(format=DATE_FORMAT))
        await create_user(user)
        await state.set_state(RegistrationStateGrope.Wallet)
        await message.answer('Введите Ваши кошельки/карты через запятые.', reply_markup=RegistrationWalletKeyboard.keyboard)


async def main():
    
    dp = Dispatcher()

    from services.registration import registration
    from services.account import account
    from services.operation import operation

    dp.include_routers(main_router, registration, account, operation)

    bot = Bot(token=TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())