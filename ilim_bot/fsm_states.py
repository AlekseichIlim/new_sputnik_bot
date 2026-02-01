from aiogram.fsm.state import State, StatesGroup


class Administration(StatesGroup):

    brigade = State()
    old_monthly_data = State()
    old_monthly_data_plan = State()
    old_monthly_finish_data = State()
    new_data = State()


class UserRegistration(StatesGroup):

    tab_number = State()


class UserGetData(StatesGroup):

    get_old_data = State()
    get_now_data = State()
    # text = {
    #     'CompanyRegister:name': 'Введите название заново:',
    #     'CompanyRegister:description': 'Введите описание заново:',
    #     'CompanyRegister:city': 'Введите название города заново:',
    #     'CompanyRegister:addresses_street': 'Введите название улицы заново:',
    #     'CompanyRegister:addresses_home': 'Введите номер дома заново:',
    #     'CompanyRegister:addresses_comment': 'Введите комментарий к адресу заново:',
    #     'CompanyRegister:phone': 'Введите номер телефона заново:',
    #
    # }


class CategoryCreate(StatesGroup):
    name_category = State()

    text = {
        'CategoryCreate:name_category': 'Введите название категории заново:',
    }


class ProductCreate(StatesGroup):
    name_category = State()
    name_product = State()
    photo_product = State()
    price = State()
    ingredients = State()

    weight = State()

    text = {
        'ProductCreate:name_product': 'Введите название блюда заново:',
        'ProductCreate:photo_product': 'Загрузите фото блюда заново:',
        'ProductCreate:ingredients': 'Введите ингредиенты блюда заново:',
        'ProductCreate:price': 'Введите цену блюда заново:',
        'ProductCreate:weight': 'Введите вес блюда заново:',
    }


class DataCompany(StatesGroup):
    view_data_company = State()
    update_data_company = State()

    text = {
        'name': 'Введите название:',
        'description': 'Введите описание:',
        'city': 'Введите название города:',
        'addresses_street': 'Введите название улицы:',
        'addresses_home': 'Введите номер дома:',
        'addresses_comment': 'Введите комментарий к адресу:',
        'phone': 'Введите номер телефона:',

    }

