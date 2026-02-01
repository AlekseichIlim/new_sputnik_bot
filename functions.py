import calendar
import os
import tempfile
from calendar import monthrange
from datetime import datetime, timedelta
import pandas as pd

from config import dict_months

cl = calendar.Calendar()


def get_count_day_month(month):
    """
    Возвращает количество дней переданного месяца текущего года.

    :param month: Число, номер месяца
    :return: Число, количество дней
    """

    year_today = datetime.now().year
    count_days = (monthrange(year_today, month))[1]

    return count_days


def get_num_month_old():
    """
        Возвращает номер предыдущего месяца

        :return: Число
    """
    num_month = datetime.now().month - 1

    if num_month == 0:
        return 12
    else:
        return num_month


def get_name_month_now(month):
    """
    Возвращает название месяца

    :param month: Число, номер месяца
    :return: Строка, название месяца на русском
    """

    name_month = dict_months[month]
    return name_month


def get_name_month_old():
    """
    Возвращает название предыдущего месяца
    :return: Строка, название месяца на русском
    """
    num_month = datetime.now().month - 1

    if num_month == 0:
        return dict_months[12]
    else:
        return dict_months[num_month]


def get_list_weeks_start_days(day, month):
    """
    Возвращает списки дат рабочей вахты в зависимости от дня заезда бригады
    0 - понедельник, 1 - вторник, 2 - среда, 3 - четверг, 4 - пятница, 5 - суббота, 6 - воскресенье

    :param day: Число, номер дня заезда
    :param month: Число, номер месяца
    :return: Список списков дат дней вахты, разделенных в зависимости от дня заезда
    """

    rez = list(cl.itermonthdays2(2025, month))
    finish_day = calendar.monthrange(2025, month)[1]

    start_day = day
    days = []
    one_week = []
    weeks = []

    for day in rez:
        if day[0] != 0:
            if day[1] == start_day:
                days.append(day)
    data_one_day = days[0][0]

    if data_one_day > 1:
        for i in range(1, data_one_day):
            one_week.append(i)
        one_week.append(data_one_day)
    else:
        one_week.append(1)
        for i in range(2, 8):
            one_week.append(i)
    weeks.append(one_week)

    for i in range(len(days)):
        week_d = []
        a = days[i][0]
        if days[i][0] != finish_day:
            while a < days[i][0] + 7:
                a += 1
                week_d.append(a)
                if a == finish_day:
                    break
        if len(week_d) == 0:
            break
        weeks.append(week_d)

    return weeks


def get_day_plan(month_plan, count_days):
    """
    Возвращает значение суточного плана

    :param month_plan: Число, значение месячного плана
    :param count_days: Число, количество дней переданного месяца
    :return: Число, значение суточного плана
    """

    a = month_plan
    b = count_days
    c = int(a/b)

    return c


async def reed_data_people_brigade(bot, message):
    """
    Читает переданный файл и записывает данные в список словарей. Ключами в словаре, являются заголовки столбцов

    :param bot: чат-бот
    :param message: message
    :param file_info: информация об отправленном файле
    :return: список словарей, каждый словарь - это объект(член бригады)
    """

    file_info = await bot.get_file(message.document.file_id)
    file_path = file_info.file_path

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        await bot.download_file(file_path, tmp.name)

        try:
            df = pd.read_excel(tmp.name, sheet_name='Лист1')
            people_dict = df.to_dict('records')

        except Exception as e:
            await message.answer(f'Ошибка чтения файла: {str(e)}')

        return people_dict


async def read_data_fullings(sheet):
    """
    Читает данные по ВПМ и записывает их в словарь
    :param sheet: страница документа
    :return: словарь, где значение ключа - список данных по ВПМ
    """
    str_index = 5
    column_index_fullings = 4
    str_code_mashine = 7
    str_operator = 8
    str_eff_time = 12
    str_volume = 84
    fullings_dict = {}

    while True:
        index_mashine = sheet.iloc[str_index, column_index_fullings]

        if 'ВПМ' in index_mashine:
            code_mashine = sheet.iloc[str_code_mashine, column_index_fullings]
            operator = sheet.iloc[str_operator, column_index_fullings]
            eff_time = sheet.iloc[str_eff_time, column_index_fullings]
            volume = sheet.iloc[str_volume, column_index_fullings]
            fullings_dict[f'{index_mashine}'] = [code_mashine, operator, round(float(eff_time), 1), volume]
        else:
            break
        column_index_fullings += 2

    return fullings_dict
