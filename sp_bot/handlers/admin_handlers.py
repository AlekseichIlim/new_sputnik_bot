from ReadFiles import ReadFilesShifts, ReadFilesPeople
from config import dict_months
from functions import get_count_day_month, get_name_month_old, get_num_month_old
from ilim_bot.filtres.admin_filter import IsAdminFilter
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
import sp_bot.keyboards.sp_bot_kb as admin_kb
from aiogram.fsm.context import FSMContext
from sp_bot.fsm_states import Administration

from ilim_bot.requests import get_one_object, save_peoples_brigade
from models.models import Brigade
from datetime import datetime

admin_router_sp = Router()

# admin_router_sp.message.filter(IsAdminFilter())


async def process_month_selection(
        state: FSMContext
) -> dict:
    """
    Обработка выбора месяца
    Возвращает данные о выбранном месяце для дальнейшего использования
    """

    month_num = get_num_month_old()

    data = {
        'month_num': month_num,
        'month_name': dict_months[month_num]
    }

    await state.update_data(**data)
    return data

@admin_router_sp.message(CommandStart())
async def admin_start(message: Message):

    await message.answer(
        f"Привет!", reply_markup=admin_kb.menu
    )


@admin_router_sp.message(F.text == 'Загрузить данные')
async def administration_data(message: Message, state: FSMContext):
    await process_month_selection(state)
    data = await state.get_data()
    await message.answer(f"Загрузи сменные рапорта за {data['month_name'].lower()}")
    await state.set_state(Administration.report_data)


@admin_router_sp.message(F.document & F.document.file_name.endswith('.xlsx'), Administration.report_data)
async def load_file_report_data(message: Message, state: FSMContext):

    data = await state.get_data()

    file = ReadFilesShifts(bot=message.bot, message=message)
    shifts_dict = await file.read_old_data_shifts_for_sp_bot(data['month_num'])
    if shifts_dict:
        await message.answer(f"Рапорта загружены")
        await state.set_state(Administration.old_monthly_finish_data)
        await message.answer(f"Загрузи итоги месяца")
    else:
        await message.answer("⚠ Не удалось прочитать файл.")
        await admin_start(message)


#
# @admin_router.message(F.text == 'Загрузка данных за прошлый месяц')
# async def administration_data_old_month(message: Message):
#     await message.answer('Выбери действие',
#                          reply_markup=await admin_kb.admin_menu_2)
#
#

@admin_router_sp.message(F.document & F.document.file_name.endswith('.xlsx'), Administration.old_monthly_finish_data)
async def load_shifts(message: Message, state: FSMContext):
    data = await state.get_data()

    file = ReadFilesShifts(bot=message.bot, message=message)
    shifts_dict = await file.read_old_data_shifts(data['month_num'], data['brigade_id'])

    if shifts_dict:
        await save_peoples_brigade(shifts_dict, data['brigade_id'])
        await message.answer(f"Рапорта {data['brigade_name']} загружены")
    else:
        await message.answer("⚠ Не удалось прочитать файл.")
    await state.clear()
    await admin_start(message)
# #####################################################
#
#
# @admin_router.message(F.text == 'Загрузка показателей прошедшего месяца')
# async def load_plan_and_finish_data(message: Message, state: FSMContext):
#     await message.answer('Выбери бригаду',
#                          reply_markup=await admin_kb.names_brigades())
#     await state.set_state(Administration.old_monthly_data_plan)
#
#
# @admin_router.callback_query(F.data.startswith('brigade_'), Administration.old_monthly_data_plan)
# async def push_brigade_load_plan(callback: CallbackQuery, state: FSMContext):
#     await process_brigade_selection(callback, state)
#     await callback.message.answer('Выбери месяц',
#                          reply_markup=await admin_kb.names_months())
#
#
# @admin_router.callback_query(F.data.startswith('month_'), Administration.old_monthly_data_plan)
# async def push_month_load_plan(callback: CallbackQuery, state: FSMContext):
#     await process_month_selection(callback, state)
#     data = await state.get_data()
#     await callback.message.answer(f"Введи плановый объем бригады {data['brigade_name']} за {data['month_name']}",
#                                   reply_markup=admin_kb.cancellation)
#
#
# @admin_router.message(Administration.old_monthly_data_plan)
# async def input_plan(message: Message, state: FSMContext):
#     await state.update_data(plan=message.text)
#
#     data = await state.get_data()
#     await state.set_state(Administration.old_monthly_finish_data)
#     await message.answer(f"Загрузи справку на ЗП бригады {data['brigade_name']} за {data['month_name']}",
#                                   reply_markup=admin_kb.cancellation)
#
#
# @admin_router.message(F.document & F.document.file_name.endswith('.xlsx'), Administration.old_monthly_finish_data)
# async def load_finish_data(message: Message, state: FSMContext):
#     data = await state.get_data()
#
#     file = ReadFilesShifts(bot=message.bot, message=message)
#
#
# ###############################
# @admin_router.message(F.text == 'Отмена')
# async def unlock_update_brigade(message: Message):
#     await administration(message)
#
#
# @admin_router.message(F.text == 'Назад')
# async def back(message: Message, state: FSMContext):
#     await state.clear()
#     await admin_start(message)
#
