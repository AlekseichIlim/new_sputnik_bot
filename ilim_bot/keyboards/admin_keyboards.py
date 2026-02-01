from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

import ilim_bot.requests as rq
from config import dict_months
from models.models import Brigade

menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Администрирование')],
                                     [KeyboardButton(text='Просмотр данных')]
                                     ], resize_keyboard=True)

admin_menu_1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Загрузка данных текущего месяца')],
                                           [KeyboardButton(text='Редактировать членов бригады')],
                                           [KeyboardButton(text='Загрузка данных за прошлый месяц')],
                                           [KeyboardButton(text='Назад')]
                                           ], resize_keyboard=True)

admin_menu_2 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Загрузка рапортов прошедшего месяца')],
                                             {KeyboardButton(
                                                 text='Загрузка показателей прошедшего месяца')},
                                           [KeyboardButton(text='Назад')]
                                           ], resize_keyboard=True)

cancellation = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отмена')]
                                             ], resize_keyboard=True)


async def names_brigades():
    all_brigades = await rq.get_all_objects(Brigade)
    keyboard = InlineKeyboardBuilder()
    for brigade in all_brigades:
        keyboard.add(InlineKeyboardButton(text=brigade.name, callback_data=f'brigade_{brigade.id}'))
    keyboard.add(InlineKeyboardButton(text='Назад\U00002b05', callback_data='to_back_main_menu'))
    return keyboard.adjust(2).as_markup()


async def names_months():
    month_now = datetime.now().month
    keyboard = InlineKeyboardBuilder()
    for month in range(1, month_now):
        keyboard.add(InlineKeyboardButton(text=dict_months[month], callback_data=f'month_{month}'))
    keyboard.add(InlineKeyboardButton(text='Назад\U00002b05', callback_data='to_back_main_menu'))
    return keyboard.adjust(2).as_markup()

