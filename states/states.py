from aiogram.fsm.state import StatesGroup, State


# Состояния формы регистрации
class RegistrationStates(StatesGroup):
    fill_have_card = State()
    fill_show_variations = State()
    fill_send_notifications = State()


# Состояния диалога главного меню
class MainMenuDialogStates(StatesGroup):
    main_menu = State()
    about = State()


# Состояния диалога админ-панели
class AdminDialogStates(StatesGroup):
    statistic = State()
    add_admin = State()


# Состояния диалога настроек
class SettingsDialogStates(StatesGroup):
    all_settings = State()
    have_card = State()
    show_variants = State()
    send_notifications = State()


# Состояния диалога избранного
class FavoritesDialogStates(StatesGroup):
    favorites_show = State()
    favorites_edit = State()


# Состояния диалога товаров
class ProductsDialogStates(StatesGroup):
    product_get_id = State()
    product_search = State()
    product_detail = State()
