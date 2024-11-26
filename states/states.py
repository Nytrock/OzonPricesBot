from aiogram.fsm.state import StatesGroup, State


class FSMRegistrationForm(StatesGroup):
    fill_have_card = State()
    fill_show_variations = State()
    fill_show_product_image = State()
    fill_send_notifications = State()


class FSMDialog(StatesGroup):
    main_menu = State()
    settings = State()
    favorites = State()
    admin_users = State()
    admin_products = State()
