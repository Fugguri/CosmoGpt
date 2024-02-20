import datetime
from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher import FSMContext

from utils import gpt, lava, find_email
from database.Database import UserManager
from config.config import Config
from keyboards.keyboards import Keyboards
from .admin import admin


async def start(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: UserManager = ctx_data.get()['db']
    try:
        db.add_user(message.from_user.id, message.from_user.username,
                    message.from_user.first_name, message.from_user.last_name)
    except Exception as ex:
        print(ex)
    await message.answer("Добро пожаловать, я помогу тебе разобраться в косметологии. Спрашивай все, что тебе интересно.")


async def create_response(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    answer = await gpt.create_answer(message)
    await message.answer(answer)


async def promo_code(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    await message.answer("Отправьте промокод")
    await state.set_state("wait_promo_code")


async def wait_promo_code(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: UserManager = ctx_data.get()['db']
    day = None
    if message.text == "FREE":
        db.update_user(message.from_user.id, free=True, use_promo=True)
    elif message.text == "МОЛЕКУЛА":
        day = datetime.datetime.utcnow() + datetime.timedelta(days=31)
    elif message.text == "ХИМИК":
        day = datetime.datetime.utcnow() + datetime.timedelta(days=91)
    else:
        await message.answer("Промокод не существует")
        return
    if day:
        db.update_user(message.from_user.id,
                       subscription_end=day, use_promo=True)
    await message.answer(f'Промокод "{message.text}" применен', reply_markup=types.ReplyKeyboardRemove())

    await state.finish()


async def subscription(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    await message.answer("Отправьте email на который придет уведомление об оплате")
    await state.set_state("wait_email")


async def wait_email(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: UserManager = ctx_data.get()['db']

    try:
        email = find_email(message.text)
        if not email:
            await message.answer("Ошибка!\nУбедитесь, что введет верный email.")
            return
    except:
        await message.answer("Ошибка!\nУбедитесь, что введет верный email.")
        return
    await state.finish()
    invoice = lava.get_invoice(email)
    print(invoice)
    contract_id = invoice.get("id")
    db.update_user(telegram_id=message.from_user.id,
                   contract_id=contract_id)

    await message.answer(f"Перейдите по ссылке и оплатите подписку.<b>\n{invoice.get('paymentUrl')}</b>", reply_markup=types.ReplyKeyboardRemove())


def register_user_handlers(dp: Dispatcher, kb: Keyboards):
    dp.register_message_handler(promo_code, text="Промокод", state="*")
    dp.register_message_handler(subscription, text="Подписка", state="*")
    dp.register_message_handler(wait_promo_code, state="wait_promo_code")
    dp.register_message_handler(wait_email, state="wait_email")
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(create_response, state="*")
