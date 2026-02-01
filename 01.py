import asyncio
from datetime import datetime, timedelta

from ReadFiles import ReadFilesShifts
from config import pl_list
from functions import get_day_plan, read_data_fullings, get_count_day_month
import calendar
import openpyxl
import pandas as pd
from math import isnan
import numpy as np

from ilim_bot.requests import get_one_object, get_user_for_number, save_tg_id_user, get_brigades_for_pl
from models.models import Brigade

# path = 'C:/Users/User1/Desktop/расчетки/Декабрь/УЛ Спутник.xlsx'
# path = 'C:/Users/User1/Desktop/расчетки/Тест рапорта.xlsx'

cl = calendar.Calendar()

num = datetime.now().month
print(type(num))
# sheet = pd.read_excel(path, sheet_name='2')

# str_date_shift = 0
# str_index_shift = 1
#
#
#
# def search_column_processor(sheet, str_index):
#     value = "Процессоp 1"
#
#     row = sheet.iloc[str_index]
#     column_name = row[row == value].index[0]
#     column = int(column_name.split('Unnamed: ')[1])
#     return column
#
# column_data = 32
# row_index = 5
# row_value = 84
#
# # index = sheet.iloc[row_index, column_data]
# # value_1 = sheet.iloc[row_value, column_data + 1]
# # value_2 = sheet.iloc[row_value, column_data + 3]
# # column = int(column_name.split('Unnamed: ')[1])
# # print(index)
#
#
# # column_data_shift = search_column_processor(sheet, row_index)
#
# str_volume = 84
# # volume_1 = sheet.iloc[str_volume, column_data_shift]
# # volume_2 = sheet.iloc[str_date_shift, column_data_shift]
# # print(volume_1)
# # a = asyncio.run(get_one_object(Brigade, 1))
# # print(a.pl)
#
# ######################################
# path = 'C:/Users/User1/Desktop/расчетки/Тест рапорта.xlsx'
# # sheet = pd.read_excel(path, sheet_name='2')
#
# # count_read_sheets = 7
# # day_now = datetime.now().day
# # if day_now < 7:
# #     count_read_sheets = day_now
# #
# # print(day_now)
# numb = '40411966'
# # a = asyncio.run(get_user(numb))
# # tg_id = 100
# # asyncio.run(save_tg_id_user(numb, tg_id))
# pl_number = 4
# a = asyncio.run(get_brigades_for_pl(pl_number))
#
# for i in a:
#     print(i.name)
# if a:
#     print(a.name, a.tg_id)
# else:
#     print('no')

# vdfbgdf