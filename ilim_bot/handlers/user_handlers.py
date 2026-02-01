from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import ilim_bot.keyboards.user_keyboards as user_kb
from aiogram.fsm.context import FSMContext

from ilim_bot.fsm_states import UserRegistration, UserGetData
from ilim_bot.handlers.admin_handlers import process_brigade_selection, process_month_selection
from ilim_bot.requests import get_all_objects, get_user_for_number, save_tg_id_user, get_user_for_tg, get_one_object
from models.models import User, Brigade
import ilim_bot.keyboards.admin_keyboards as admin_kb

user_router = Router()


# admin_router.message.filter(IsAdminFilter())


@user_router.message(CommandStart())
async def user_start(message: Message):
    tg_id = message.from_user.id
    user = await get_user_for_tg(tg_id)
    if user:
        await message.answer(
            "Информация за какой месяц вас интересует?", reply_markup=user_kb.months
        )
    else:
        await message.answer(
            "Привет, этот бот предоставляет информацию о производственных показателях лесозаготовительных бригад"
        )
        await message.answer(
            "Для того чтобы получить доступ к функционалу бота сначала нужно зарегистрироваться."
            "\nДля этого нажмите на кнопку <Регистрация>",
            reply_markup=user_kb.registration
        )


@user_router.message(F.text == 'Регистрация')
async def user_registration(message: Message, state: FSMContext):
    await message.answer('Введите свой восьмизначный табельный номер, например: 40******'
                         )
    await state.set_state(UserRegistration.tab_number)


@user_router.message(UserRegistration.tab_number)
async def input_tab_number(message: Message, state: FSMContext):
    await state.update_data(tab_number=message.text)
    data = await state.get_data()
    tab_number = data['tab_number']
    user = await get_user_for_number(tab_number)
    if user:
        await state.update_data(user=user)
        await message.answer(f'Это вы, {user.surname} {user.name} {user.patronymic} пытаетесь зарегистрироваться?',
                             reply_markup=user_kb.yes_or_no)
    else:
        await message.answer('Вашего табельного номера нет в базе данных. Обратитесь к руководству.')
        await state.clear()
        await user_start(message)


@user_router.callback_query(F.data == 'yes', UserRegistration.tab_number)
async def press_yes(message: Message, state: FSMContext):
    data = await state.get_data()
    tg_id = message.from_user.id
    tab_numb = data['tab_number']
    user = data['user']
    brigade = await get_one_object(Brigade, user.brigade)
    if user.post == 'Руководитель':
        await message.answer(f'Регистрация завершена успешно\n{user.surname} {user.name} {user.patronymic}\n'
                             f'Табельный номер: {user.tab_number}\nРуководитель ПЛ №{brigade.pl}'
                             )
    else:
        await message.answer(f'Регистрация завершена успешно\n{user.surname} {user.name} {user.patronymic}\n'
                             f'Табельный номер: {user.tab_number}\nБригада: {brigade.name}'
                             )
    await save_tg_id_user(tab_numb, tg_id)
    await state.clear()
    await message.answer(
        "Информация за какой месяц вас интересует?", reply_markup=user_kb.months
    )


@user_router.message(F.text == 'Предыдущий')
async def selection_old_month(message: Message, callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserGetData.get_old_data)
    tg_id = message.from_user.id
    user = await get_user_for_tg(tg_id)
    await state.update_data(user=user)
    await message.answer('Выбери месяц',
                            reply_markup=await admin_kb.names_months())
    await process_month_selection(callback, state)


@user_router.callback_query(F.data.startswith('month_'), UserGetData.get_old_data)
async def get_old_data(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = data['user']
    month_num = data['month_num']
    brigade_id = user.brigade
    if user.post == 'Руководитель':
        await callback.message.answer('Выбери Бригаду',
                            reply_markup=await admin_kb.names_brigades())
        await process_brigade_selection(callback, state)
    else:
        # получение данных за прошлый месяц
        await state.clear()


@user_router.callback_query(F.data.startswith('brigade_'), UserGetData.get_old_data)
async def selection_brigade_1(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    brigade_id = data['brigade_id']
    month_num = data['month_num']
    # получение данных за прошлый месяц выбранной бригады
    await state.clear()


@user_router.message(F.text == 'Текущий')
async def selection_now_month(message: Message, callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserGetData.get_now_data)
    tg_id = message.from_user.id
    user = await get_user_for_tg(tg_id)
    await state.update_data(user=user)
    if user.post == 'Руководитель':
        await callback.message.answer('Выбери Бригаду',
                                      reply_markup=await admin_kb.names_brigades())
        await process_brigade_selection(callback, state)
    else:
        await callback.message.answer('Какую информацию предоставить?',
                                        reply_markup=user_kb.now_month_data)


@user_router.callback_query(F.data.startswith('brigade_'), UserGetData.get_now_data)
async def selection_brigade_2(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Какую информацию предоставить?',
                                  reply_markup=user_kb.now_month_data)
    # получение данных за текущий месяц выбранной бригады

#############

@user_router.message(F.data == 'no', UserRegistration.tab_number)
async def press_no(message: Message, state: FSMContext):
    await message.answer(f'Проверьте введенный вами табельный номер или обратитесь к руководству'
                         )
    await state.clear()
    await user_start(message)
