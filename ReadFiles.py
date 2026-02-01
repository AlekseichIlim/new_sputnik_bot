import tempfile
import pandas as pd
from math import isnan
import numpy as np
from functions import get_count_day_month
from ilim_bot.requests import get_one_object
from models.models import Brigade


class ReadFiles:

    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    async def clean_value(self, value):
        if isinstance(value, (float, np.floating)) and isnan(value):
            return None
        return value

    async def get_download_file(self):
        """Возвращает загруженный в бот файл"""

        file_info = await self.bot.get_file(self.message.document.file_id)
        file_path = file_info.file_path

        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            await self.bot.download_file(file_path, tmp.name)
            return tmp.name


class ReadFilesPeople(ReadFiles):

    async def read_data_people_brigade(self):
        """
        Читает переданный файл и записывает данные в список словарей. Ключами в словаре, являются заголовки столбцов

        :return: список словарей, каждый словарь - это объект(член бригады)
        """

        try:
            file_path = await self.get_download_file()
            df = pd.read_excel(file_path, sheet_name='Лист1')
            people_dict = df.to_dict('records')
            return people_dict

        except Exception as e:
            await self.message.answer(f'Ошибка чтения файла: {str(e)}')
            return []


class ReadFilesShifts(ReadFiles):
    column_data_shift = 3 #данные смены
    str_date_shift = 0 #дата смены
    str_index_shift = 1 #индекс смены

    str_index = 5 #индекс машин

    str_code_mashine = 7 #код машины
    str_operator = 8 #оператор
    str_eff_time = 12 #эффективное время
    str_volume = 84 #объем

    # async def read_data_fullings(self, sheet):
    #     """
    #     Читает данные по ВПМ и записывает их в словарь
    #     :param sheet: страница
    #     :return: словарь, где значение ключа - список данных по ВПМ
    #     """
    #     column_start = 4  # столбец впм
    #     max_columns = sheet.shape[1]
    #     print(max_columns)
    #     fullings_list = []
    #     processor_list = []
    #     while column_start < max_columns:
    #         print(column_start)
    #         index_mashine = sheet.iloc[self.str_index, column_start]
    #         print(index_mashine)
    #
    #         if 'ВПМ' in index_mashine:
    #             code_mashine = await self.clean_value(sheet.iloc[self.str_code_mashine, column_start])
    #             operator = await self.clean_value(sheet.iloc[self.str_operator, column_start])
    #             eff_time = await self.clean_value(sheet.iloc[self.str_eff_time, column_start])
    #             volume = await self.clean_value(sheet.iloc[self.str_volume, column_start])
    #             if code_mashine and operator is not None:
    #                 fullings_list.append([str(code_mashine), str(operator), round(float(eff_time), 1),
    #                                       int(volume)])
    #             else:
    #                 fullings_list.append([code_mashine, operator, round(float(eff_time), 1),
    #                                       int(volume)])
    #             column_start += 2
    #             print(fullings_list)
    #         elif 'Скиддер' in index_mashine:
    #             column_start += 2
    #             continue
    #         elif 'Процессор' in index_mashine:
    #             code_mashine = await self.clean_value(sheet.iloc[self.str_code_mashine, column_start])
    #             operator = await self.clean_value(sheet.iloc[self.str_operator, column_start])
    #             eff_time = await self.clean_value(sheet.iloc[self.str_eff_time, column_start])
    #             volume_1 = await self.clean_value(sheet.iloc[self.str_volume, column_start + 1])
    #             volume_2 = await self.clean_value(sheet.iloc[self.str_volume, column_start + 3])
    #             volume = int(volume_1) + int(volume_2)
    #             if code_mashine and operator is not None:
    #                 processor_list.append([str(code_mashine), str(operator), round(float(eff_time), 1),
    #                                        int(volume)])
    #             else:
    #                 processor_list.append([code_mashine, operator, round(float(eff_time), 1),
    #                                        int(volume)])
    #             column_start += 4
    #             print(processor_list)
    #
    #         else:
    #             break
    #
    #     print(fullings_list)
    #     print(processor_list)
    #
    #     return fullings_list, processor_list

    # async def read_data_mashins(self, sheet):
    #     """
    #     Читает данные по машинам и записывает их в словарь`
    #     :param sheet: страница
    #     :return: словарь, где значение ключа - список данных
    #     """
    #     column_start = 4  # столбец впм
    #     max_columns = sheet.shape[1]
    #     print(max_columns)
    #     mashine_list = []
    #     while column_start < max_columns:
    #         print(column_start)
    #         index_mashine = sheet.iloc[self.str_index, column_start]
    #         print(index_mashine)
    #
    #         if 'ВПМ' in index_mashine:
    #             code_mashine = await self.clean_value(sheet.iloc[self.str_code_mashine, column_start])
    #             if code_mashine is not None:
    #                 operator = await self.clean_value(sheet.iloc[self.str_operator, column_start])
    #                 eff_time = await self.clean_value(sheet.iloc[self.str_eff_time, column_start])
    #                 volume = await self.clean_value(sheet.iloc[self.str_volume, column_start])
    #
    #                 mashine_list.append([str(code_mashine), str(operator), round(float(eff_time), 1),
    #                                     int(volume)])
    #                 column_start += 2
    #             else:
    #                 column_start += 2
    #                 continue
    #             print(mashine_list)
    #         elif 'Скиддер' in index_mashine:
    #             column_start += 2
    #             continue
    #         elif 'Процессор' or 'Харвестер' in index_mashine:
    #             code_mashine = await self.clean_value(sheet.iloc[self.str_code_mashine, column_start])
    #             if code_mashine is not None:
    #                 operator = await self.clean_value(sheet.iloc[self.str_operator, column_start])
    #                 eff_time = await self.clean_value(sheet.iloc[self.str_eff_time, column_start])
    #                 volume_1 = await self.clean_value(sheet.iloc[self.str_volume, column_start + 1])
    #                 volume_2 = await self.clean_value(sheet.iloc[self.str_volume, column_start + 3])
    #                 volume = int(volume_1) + int(volume_2)
    #
    #                 mashine_list.append([str(code_mashine), str(operator), round(float(eff_time), 1),
    #                                      int(volume)])
    #                 column_start += 4
    #                 print(mashine_list)
    #             else:
    #                 column_start += 4
    #                 continue
    #
    #         elif 'Форвардер' in index_mashine:
    #             code_mashine = await self.clean_value(sheet.iloc[self.str_code_mashine, column_start])
    #             if code_mashine is not None:
    #                 operator = await self.clean_value(sheet.iloc[self.str_operator, column_start])
    #                 eff_time = await self.clean_value(sheet.iloc[self.str_eff_time, column_start])
    #                 volume_1 = await self.clean_value(sheet.iloc[self.str_volume, column_start])
    #                 volume_2 = await self.clean_value(sheet.iloc[self.str_volume, column_start + 1])
    #                 volume_3 = await self.clean_value(sheet.iloc[self.str_volume, column_start + 2])
    #                 volume_4 = await self.clean_value(sheet.iloc[self.str_volume, column_start + 3])
    #                 volume = int(volume_1) + int(volume_2) + int(volume_3) + int(volume_4)
    #
    #                 mashine_list.append([str(code_mashine), str(operator), round(float(eff_time), 1),
    #                                            int(volume)])
    #                 column_start += 4
    #                 print(mashine_list)
    #             else:
    #                 column_start += 4
    #                 continue
    #
    #         else:
    #             break
    #
    #     print(fullings_list)
    #     print(processor_list)
    #
    #     return fullings_list, processor_list

    async def read_data_mashins(self, sheet):
        """
        Читает данные по машинам и записывает их в словарь`
        :param sheet: страница
        :return: словарь, где значение ключа - список данных
        """
        column_start = 4  # столбец впм
        max_columns = sheet.shape[1]
        machine_list = []
        while column_start < max_columns:

            index_machine = sheet.iloc[self.str_index, column_start]
            code_machine = await self.clean_value(sheet.iloc[self.str_code_mashine, column_start])

            if code_machine is not None:

                eff_time = await self.clean_value(sheet.iloc[self.str_eff_time, column_start])
                operator = await self.clean_value(sheet.iloc[self.str_operator, column_start])

                if 'Погрузчик' in index_machine or 'Бульдозер' in index_machine:
                    break

                elif operator is None:
                    column_start += 2
                    continue

                elif 'ВПМ' in index_machine:
                    volume = await self.clean_value(sheet.iloc[self.str_volume, column_start])
                    column_start += 2

                elif 'Скиддер' in index_machine:
                    column_start += 2
                    continue

                elif 'Процессор' or 'Харвестер' in index_machine:
                    volume_proc_1 = await self.clean_value(sheet.iloc[self.str_volume, column_start + 1])
                    volume_proc_2 = await self.clean_value(sheet.iloc[self.str_volume, column_start + 3])
                    volume = int(volume_proc_1) + int(volume_proc_2)
                    column_start += 4

                elif 'Форвардер' in index_machine:
                    volume_1 = await self.clean_value(sheet.iloc[self.str_volume, column_start])
                    volume_2 = await self.clean_value(sheet.iloc[self.str_volume, column_start + 1])
                    volume_3 = await self.clean_value(sheet.iloc[self.str_volume, column_start + 2])
                    volume_4 = await self.clean_value(sheet.iloc[self.str_volume, column_start + 3])
                    volume = int(volume_1) + int(volume_2) + int(volume_3) + int(volume_4)
                    column_start += 4
                    print(f'{operator}: {eff_time} - {volume}')

                else:
                    column_start += 2
                    continue

                machine_list.append([str(code_machine), str(operator), round(float(eff_time), 1),
                                     int(volume)])

            else:
                column_start += 2
                continue
        return machine_list

    async def read_old_data_shifts(self, month, brigade_id):
        """
        Читает данные смены и записывает их в словарь
        :param month: int, номер месяца
        :param brigade: int, id бригады
        :return: словарь, где значение ключа - список данных за смену
        """

        count_sheets = int(get_count_day_month(month)) * 2
        shifts = {}
        path = await self.get_download_file()
        for number_sheet in range(1, count_sheets + 1):
            try:
                sheet = pd.read_excel(path, sheet_name=str(number_sheet))

                index_shift = sheet.iloc[self.str_index_shift, self.column_data_shift]
                date_shift = sheet.iloc[self.str_date_shift, self.column_data_shift].date()
                machines_data = await self.read_data_mashins(sheet)
                brigade = await get_one_object(Brigade, brigade_id)
                pl = brigade.pl

                shifts[str(number_sheet)] = {
                    'date_shift': date_shift,
                    'index_shift': index_shift,
                    'brigade': brigade_id,
                    'pl': pl,
                    'month': month,
                    'machines_data': machines_data
                }

            except Exception:
                break
        return shifts

    async def read_old_data_shifts_for_sp_bot(self, month):
        """
        Читает данные смены и записывает их в словарь
        :param month: int, номер месяца
        :param brigade: int, id бригады
        :return: словарь, где значение ключа - список данных за смену
        """

        count_sheets = int(get_count_day_month(month)) * 2
        shifts = {}
        path = await self.get_download_file()
        for number_sheet in range(1, count_sheets + 1):
            try:
                sheet = pd.read_excel(path, sheet_name=str(number_sheet))

                index_shift = sheet.iloc[self.str_index_shift, self.column_data_shift]
                date_shift = sheet.iloc[self.str_date_shift, self.column_data_shift].date()
                machines_data = await self.read_data_mashins(sheet)

                shifts[str(number_sheet)] = {
                    'date_shift': date_shift,
                    'index_shift': index_shift,
                    'month': month,
                    'machines_data': machines_data
                }

            except Exception:
                break
        print(shifts)
        return shifts

    # async def read_data_shifts(self, month, brigade):
    #     """
    #     Читает данные смены и записывает их в словарь
    #     :param month: int, номер месяца
    #     :param brigade: int, id бригады
    #     :return: словарь, где значение ключа - список данных за смену
    #     """
    #
    #     count_sheets = int(get_count_day_month(month)) * 2
    #     shifts = {}
    #     for number_sheet in range(1, count_sheets + 1):
    #         try:
    #             path = await self.get_download_file()
    #             sheet = pd.read_excel(path, sheet_name=str(number_sheet))
    #
    #             index_shift = sheet.iloc[self.str_index_shift, self.column_data_shift]
    #             date_shift = sheet.iloc[self.str_date_shift, self.column_data_shift].date()
    #             fullings_data, processor_data = await self.read_data_fullings(sheet)
    #             print(fullings_data)
    #             print(processor_data)
    #             # fullings_data = await self.read_data_fullings(sheet)
    #
    #             shifts[str(number_sheet)] = {
    #                 'date_shift': date_shift,
    #                 'index_shift': index_shift,
    #                 'brigade': brigade,
    #                 'month': month,
    #                 'fullings_data': fullings_data,
    #                 'processor_data': processor_data
    #             }
    #         except Exception:
    #             break
    #     return shifts


class ReadFilesFinishData(ReadFiles):
    pass
