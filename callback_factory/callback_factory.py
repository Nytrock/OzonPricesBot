from aiogram.filters.callback_data import CallbackData


# фабрика коллбэков для кнопки в уведомлениях
class ProductCallbackFactory(CallbackData, prefix='product'):
    product_id: int
