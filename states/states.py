from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    fill_have_card = State()
    fill_show_variations = State()
    fill_show_product_image = State()
    fill_send_notifications = State()


class MainMenuDialogStates(StatesGroup):
    main_menu = State()
    about = State()


class AdminDialogStates(StatesGroup):
    statistic = State()
    add_admin = State()


class SettingsDialogStates(StatesGroup):
    all_settings = State()
    have_card = State()
    show_variants = State()
    show_image = State()
    send_notifications = State()


class FavoritesDialogStates(StatesGroup):
    favorites_show = State()
    favorites_edit = State()


class ProductsDialogStates(StatesGroup):
    product_search = State()
    product_search_list = State()
    product_detail = State()
