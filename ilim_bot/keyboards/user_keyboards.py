from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

import ilim_bot.requests as rq
from config import dict_months
from models.models import Brigade

registration = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Регистрация')]
                                             ], resize_keyboard=True)

yes_or_no = InlineKeyboardMarkup(inline_keyboard=[
                                                [InlineKeyboardButton(text='Да', callback_data='yes'),
                                                 InlineKeyboardButton(text='Нет', callback_data='no')
                                                 ]
                                                ], resize_keyboard=True)

months = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Текущий месяц'), KeyboardButton(text='Предыдущий месяц')]
                                       ], resize_keyboard=True)


now_month_data = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='План на месяц')],
                                               [KeyboardButton(text='Объем заготовки с начала месяца')],
                                               [KeyboardButton(text='Посуточная заготовка')]
                                               ], resize_keyboard=True)
