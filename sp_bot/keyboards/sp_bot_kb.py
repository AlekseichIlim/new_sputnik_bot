from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Загрузить данные')]
                                     ], resize_keyboard=True)