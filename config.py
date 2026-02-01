import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from aiogram import Bot

ADMINS = [1892638646, ]
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)

DEBUG = True

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

dict_months = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август', 9: 'Сентябрь',
    10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }

pl_list = [
    {'number': 4, 'managers': ['40411964', ], 'brigades': ['Спутник', 'Спутник-2']},
    {'number': 2, 'brigades': ['Сибирь', 'Простор']}
]
