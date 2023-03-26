from datetime import date, datetime
from create_bot import dp, bot, db
from create_bot import BOT_NAME
from aiogram import types, Dispatcher
from keybords.client_kb import kb
from create_bot import KASSA_TOKEN
from aiogram.types.message import ContentType
from aiogram.types import Message, ShippingOption,ShippingQuery, LabeledPrice,PreCheckoutQuery
from aiogram.types.message import ContentType
import random
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from random import randint
from random import choice
from bs4 import BeautifulSoup
from aiogram.utils import executor
from aiogram import executor
from keybords.client_kb import in1,in2,in4,in_or,kb_chanall
import json
from db import Database
CHANALL_ID = '@genshinnothing'


def check_sub(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if check_sub(await bot.get_chat_member(chat_id=CHANALL_ID,user_id=message.from_user.id)):
        await bot.send_message(message.from_user.id,'Бот в работе',reply_markup=kb)
    else:
        await bot.send_message(message.from_user.id,'Подпишись на канал',reply_markup=kb_chanall)

    if not db.user_exists(message.from_user.id):
        start_command = message.text
        referrer_id = str(start_command[7:])
        if str(referrer_id) != '':
            if str(referrer_id) != str(message.from_user.id):
                db.add_user(message.from_user.id, referrer_id)
                try:
                    await bot.send_message(referrer_id,'+2 рубля')
                    #Сюда нужно будет добавить счетчик для пополнения баланса
                except:
                    pass
            else:
                db.add_user(message.from_user.id)
                await bot.send_message(message.from_user.id, "Нельзя регестрироваться по собственной ссылке")
        else:
            db.add_user((message.from_user.id))

    #await message.answer(f'Бот в работе', reply_markup=kb)


async def profile(message: types.Message):
    await message.answer(f'Хмм, Юзер, вот, что у тебя есть:\nБаланс:\nКупоны для розыгрыша:\nДрузья: {db.count_reeferals(message.from_user.id)} \n',reply_markup=in1)



@dp.callback_query_handler(text='d')
async def friend(message: types.Message):
    await bot.send_message(message.from_user.id,f"Твоя ссылка:https://t.me/{BOT_NAME}?start={message.from_user.id}")
    await message.answer()

@dp.callback_query_handler(text='p')
async def plus_balance(callback: types.CallbackQuery):
    await callback.message.answer(f'Для покупки введите команду /buy')
    await callback.answer()


@dp.message_handler(commands=['buy'])
async def balanc(message: types.Message):
    await bot.send_invoice(message.chat.id,
                           title='Привет в кружочке',
                           description='Одноразовый платеж',
                           provider_token=KASSA_TOKEN,
                           currency='rub',
                           need_email=False,
                           need_phone_number=False,
                           is_flexible=False,
                           prices=PRICES1,
                           start_parameter='example',
                           payload='test-invoice-payload')





@dp.pre_checkout_query_handler(lambda q: True)
async def check(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount}{message.successful_payment.currency} прошел успешно!")


PRICES1 = [
    LabeledPrice(label='Пополнение баланса', amount=10000),
]


async def luck(message: types.Message):
    await message.answer(f'Чтобы поучаствовать в розыгрыше благословения полой луны - нажимай на «розыгрыш»\nТак же здесь есть мини-игры, где ты можешь поиграть на баланс!',reply_markup=in2)


class FSMstavka(StatesGroup):
    cash = State()
    random_num = State()
    number = State()
    ston = State()
    srav = State()


@dp.callback_query_handler(text = 'or',state=None)
async def stavka(callback: types.CallbackQuery):
    await FSMstavka.cash.set()
    await callback.message.answer(f'Введи сумму ставки!(Минимальная ставка - 1р. Максимальная - 10р.)')
    await callback.answer()

@dp.message_handler(content_types=['text'],state=FSMstavka.cash)
async def cash(message: types.Message, state: FSMstavka):
    async with state.proxy() as data:
        data['cash'] = int(message.text)
        с = data['cash']
        if с >= 1 and с <= 10:
             await message.answer(f'Твоя ставка {с}! Теперь выбери сторону')
             await FSMstavka.next()
        else:
             await message.answer('Такую сумму поставить нельзя! Сделай ставку снова')


@dp.message_handler(state=FSMstavka.random_num)
async def random_num(message: types.Message, state: FSMstavka):
    async with state.proxy() as data:
        c = data['cash']
        myseq = ['Орел','Решка']
        choice(myseq)
        #с = random.randint(0,1)
        if message.text == choice(myseq):
            c = c * 2
            await message.answer(f'Победа,твой выигрышь {c}')
        else:
            await message.answer('Проигрышь')
    await state.finish()





class FSMkub(StatesGroup):
    money = State()
    random_number = State()

@dp.callback_query_handler(text = 'k',state=None)
async def stav(callback: types.CallbackQuery):
    await FSMkub.money.set()
    await callback.message.answer(f'Введи сумму ставки!')
    await callback.answer()

@dp.message_handler(content_types=['text'],state=FSMkub.money)
async def money(message: types.Message, state: FSMkub):
    async with state.proxy() as data:
        data['money'] = int(message.text)
        s = data['money']
        if s > 0:
             await message.answer(f'Твоя ставка {s}! Теперь выбери число')
             await FSMkub.next()
        else:
             await message.answer('Такую сумму поставить нельзя! Сделай ставку снова')

@dp.message_handler(state=FSMkub.random_number)
async def random_nun(message: types.Message, state: FSMkub):
    async with state.proxy() as data:
        s = data['money']
        ku = random.randint(0,5)
        await FSMstavka.next()
        if int(message.text) == ku:
            s = s * 6
            await message.answer(f'Победа,твой выигрышь {s}')
        else:
            await message.answer('Проигрышь')
    await state.finish()




async def spon(message: types.Message):
    await message.answer('Пока пусто')


async def info(message: types.Message):
    await message.answer('Пока пусто')


async def bonus(message: types.Message):
    await message.answer('Здесь ты можешь получать ежедневный бонус на свой баланс, а потом испытать свою удачу!',reply_markup=in4)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(profile, text='Профиль')
    dp.register_message_handler(luck, text='Испытать удачу')
    dp.register_message_handler(spon, text='Спонсоры')
    dp.register_message_handler(info, text='Информация')
    dp.register_message_handler(bonus, text='Ежедневный бонус')