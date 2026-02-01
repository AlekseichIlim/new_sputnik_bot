from sqlalchemy import text, inspect
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from config import DATABASE_URL, AsyncSessionLocal
from models.models import Base, DataMonth


async def delete_tables():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

async def delete_tables_model(model):
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.remove(model))
    await engine.dispose()

async def delete_obj(model, obj_id):
    async with AsyncSessionLocal() as session:
        obj = await session.get(model, obj_id)
        await session.delete(obj)
        await session.commit()


async def create_all_tables(engine):
    """
    Создает все таблицы БД
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# async def create_monthly_shifts_table(engine, year: int, month: int):
#     """
#     Создает таблицу смен для указанного месяца
#     Формат имени таблицы: shifts_YYYY_MM
#     """
#     # Формируем имя таблицы
#     table_name = f"shifts_{year}_{month:02d}"
#
#     # Создаем динамический класс
#     class Shift(ShiftBase):
#         __tablename__ = table_name
#         __table_args__ = {'extend_existing': True}
#     # Создаем таблицу в БД
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all, tables=[Shift.__table__])
#
#     return Shift


# async def drop_all_tables(engine):
#     """
#     Безопасное удаление всех таблиц в правильном порядке
#     """
#     async with engine.begin() as conn:
#         # 1. Получаем список всех таблиц через синхронный inspect
#         inspector = await conn.run_sync(lambda sync_conn: inspect(sync_conn))
#         all_tables = await inspector.get_table_names()
#
#         if not all_tables:
#             print("В базе нет таблиц для удаления")
#             return
#
#         # 2. Удаляем все таблицы с CASCADE через прямое SQL
#         for table in reversed(all_tables):  # Обратный порядок для зависимостей
#             try:
#                 await conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
#                 print(f"Успешно удалено: {table}")
#             except Exception as e:
#                 print(f"Ошибка при удалении {table}: {str(e)}")
#
#         # 3. Очищаем метаданные SQLAlchemy
#         await conn.run_sync(Base.metadata.drop_all)

# async def drop_all_tables(engine):
#     async with engine.begin() as conn:
#         # Используем run_sync для вызова синхронного drop_all
#         await conn.run_sync(Base.metadata.drop_all)
#         print("Все таблицы успешно удалены")

# engine = create_async_engine(DATABASE_URL)
# asyncio.run(delete_tables_model())

