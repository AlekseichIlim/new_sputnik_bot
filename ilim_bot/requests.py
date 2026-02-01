import asyncio
from sqlalchemy.dialects.postgresql import insert
from aiogram.types import message
from sqlalchemy import select

from config import AsyncSessionLocal
from models.models import User, Brigade, Operator, DataMonth
from sqlalchemy.exc import IntegrityError
from datetime import datetime

async def save_names_brigades(pl_list):
    """Заполнение таблицы данных бригад"""

    for pl in pl_list:
        for name in pl['brigades']:
            try:
                new_brigade = Brigade(
                    name=name,
                    pl=pl['number']
                )
                async with AsyncSessionLocal() as session:
                    session.add(new_brigade)
                    await session.commit()
            except IntegrityError:
                await session.rollback()


async def save_peoples_brigade(people_dict, brigade_id):
    """Заполнение таблицы пользователей"""

    for user in people_dict:
        try:
            new_user = User(
                name=user['имя'],
                surname=user['фамилия'],
                patronymic=user['отчество'],
                tab_number=user['табельный'],
                post=user['должность'],
                brigade=brigade_id
            )
            async with AsyncSessionLocal() as session:
                session.add(new_user)
                await session.commit()
        except IntegrityError:
            await session.rollback()


async def save_tg_id_user(tab_number, tg_id):
    """Запись tg_id пользователя в БД"""

    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.tab_number == int(tab_number)))
            user = result.scalars().first()
            user.tg_id = int(tg_id)
            await session.commit()
    except IntegrityError:
        await session.rollback()

# async def save_data_shifts(shifts_dict, message):
#     """Заполнение таблицы смен"""
#
#     count_shifts = 0
#     for shift_id, shift_data in shifts_dict.items():
#         try:
#             shift_record = {
#                 'brigade': shift_data['brigade'],
#                 'date': shift_data['date_shift'],
#                 'index': shift_data['index_shift'],
#                 'month': shift_data['month'],
#             }
#             for i, fulling in enumerate(shift_data['fullings_data'][:6], start=1):
#                 shift_record.update({
#                     f'fulling_{i}': fulling[0],
#                     f'operator_fulling_{i}': fulling[1],
#                     f'eff_time_full_{i}': fulling[2],
#                     f'volume_full_{i}': fulling[3]
#                 })
#             for i, processor in enumerate(shift_data['processor_data'][:10], start=1):
#                 shift_record.update({
#                     f'processor_{i}': processor[0],
#                     f'operator_proc_{i}': processor[1],
#                     f'eff_time_proc_{i}': processor[2],
#                     f'volume_proc_{i}': processor[3]
#                 })
#
#             # Создаем и сохраняем запись
#             new_shift = Shift(**shift_record)
#
#             async with AsyncSessionLocal() as session:
#                 session.add(new_shift)
#                 await session.commit()
#
#             count_shifts += 1
#         except IntegrityError as e:
#             await message.answer(f'ошибка - {e}.')
#             await session.rollback()
#     await message.answer(f'Загружено смен - {count_shifts}.')

# async def save_data_shifts(shifts_dict, message):
#     """Заполнение таблицы смен"""
#
#     for shift_id, shift_data in shifts_dict.items():
#         for maсhine in shift_data['machines_data']:
#             try:
#                 new_operator = Operator(
#                     brigade=shift_data['brigade'],
#                     pl=shift_data['pl'],
#                     date_shift=shift_data['date_shift'],
#                     index_shift=shift_data['index_shift'],
#                     month=shift_data['month'],
#                     index_machine=maсhine[0],
#                     name=maсhine[1],
#                     eff_time=maсhine[2],
#                     volume=maсhine[3],
#                 )
#
#                 async with AsyncSessionLocal() as session:
#                     session.add(new_operator)
#                     await session.commit()
#
#             except IntegrityError as e:
#                 await message.answer(f'ошибка - {e}.')
#                 await session.rollback()


async def save_old_data_shifts(shifts_dict, message):
    """Заполнение таблицы смен"""

    async with AsyncSessionLocal() as session:
        for shift_id, shift_data in shifts_dict.items():
            for machine in shift_data['machines_data']:
                try:
                    stmt = insert(Operator).values(
                        brigade=shift_data['brigade'],
                        pl=shift_data['pl'],
                        date_shift=shift_data['date_shift'],
                        index_shift=shift_data['index_shift'],
                        month=shift_data['month'],
                        index_machine=machine[0],
                        name=machine[1],
                        eff_time=machine[2],
                        volume=machine[3],
                    ).on_conflict_do_update(
                        constraint='uniq_id',
                        set_={
                            'name': machine[1],
                            'eff_time': machine[2],
                            'volume': machine[3],
                            # добавьте другие поля для обновления
                        }
                    )

                    await session.execute(stmt)
                    await session.commit()

                except Exception as e:
                    await message.answer(f'Ошибка - {e}.')
                    await session.rollback()


async def get_plan_now_month():

    """ Возвращает значение плана текущего месяца """
    year_today = datetime.now().year
    month_today = datetime.now().month
    async with AsyncSessionLocal() as session:
        obj = select(DataMonth).where(User.tab_number == int(tab_number))


async def get_user_for_number(tab_number):
    """ Возвращает данные юзера по табельному номеру """

    async with AsyncSessionLocal() as session:
        obj = select(User).where(User.tab_number == int(tab_number))
        result = await session.execute(obj)
        return result.scalar_one_or_none()


async def get_user_for_tg(tg_id):
    """ Возвращает данные юзера по tg_id """

    async with AsyncSessionLocal() as session:
        obj = select(User).where(User.tg_id == int(tg_id))
        result = await session.execute(obj)
        return result.scalar_one_or_none()


async def get_brigades_for_pl(pl_number):
    """ Возвращает все бригады ПЛ """
    async with AsyncSessionLocal() as session:
        obj = select(Brigade).where(Brigade.pl == int(pl_number))
        result = await session.execute(obj)
        return result.scalars().all()

async def get_all_objects(model):
    """ Возвращает все объекты модели """

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(model))
        return result.scalars().all()


async def get_one_object(model, obj_id):
    """ Возвращает объект модели """

    async with AsyncSessionLocal() as session:
        obj = select(model).where(model.id == obj_id)
        result = await session.execute(obj)
        return result.scalar_one_or_none()


async def update_one_object(model, obj_id, name_field, item_field):
    """ Изменяет объект модели """

    async with AsyncSessionLocal() as session:
        obj = select(model).where(model.id == obj_id)
        result = await session.execute(obj)
        obj_model = result.scalar_one()
        setattr(obj_model, name_field, item_field)
        await session.commit()
        return obj_model

