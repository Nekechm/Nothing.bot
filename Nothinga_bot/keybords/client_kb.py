from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from create_bot import dp

k1 = KeyboardButton('Профиль')
k2 = KeyboardButton('Информация')
k3 = KeyboardButton('Испытать удачу')
k4 = KeyboardButton('Спонсоры')
k5 = KeyboardButton('Ежедневный бонус')
k6 = KeyboardButton('Магазин')



kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(k1).insert(k2).add(k3).insert(k5).add(k4).insert(k6)

kb_chanall = InlineKeyboardMarkup(row_width=1)
kb_chanall.add(InlineKeyboardButton(text='Канал', url='https://t.me/genshinnothing'))


in1 = InlineKeyboardMarkup(row_width=3)
in1.add(InlineKeyboardButton(text='Пригласить друга',callback_data='d')).add(InlineKeyboardButton(text='Купить купоны',callback_data='k')).add(InlineKeyboardButton(text='Пополнить баланс', callback_data='p'))

in2 = InlineKeyboardMarkup(row_width=3)
in2.add(InlineKeyboardButton(text='Розыгрыш',callback_data='r')).add(InlineKeyboardButton(text='Орел или Решка',callback_data='or')).add(InlineKeyboardButton(text='Кубик(x6)',callback_data='k'))

in_or = InlineKeyboardMarkup(row_width=2)
in_or.add(InlineKeyboardButton(text='Орел',callback_data='orel')).add(InlineKeyboardButton(text='Решка',callback_data='reshka'))


in4 = InlineKeyboardMarkup(row_width=1)
in4.add(InlineKeyboardButton(text='Получить награду', callback_data='n'))

