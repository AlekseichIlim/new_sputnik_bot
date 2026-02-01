from aiogram import types
from aiogram.filters import Filter
from config import ADMINS


class IsAdminFilter(Filter):
    """
    Фильтр для проверки, является ли пользователь админом
    """
    async def __call__(self, message: types.Message):
        return message.from_user.id in ADMINS
