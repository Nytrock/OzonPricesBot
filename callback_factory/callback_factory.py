from aiogram.filters.callback_data import CallbackData


class ProductCallbackFactory(CallbackData, prefix='product'):
    product_id: int
