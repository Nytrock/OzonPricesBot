from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from database.methods import update_have_card, update_show_variations, update_send_notifications


async def update_user_have_card(_: CallbackQuery, button: Button, manager: DialogManager) -> None:
    user_id = manager.event.from_user.id
    have_card = button.widget_id == 'on'
    manager.middleware_data['user_have_card'] = have_card
    await update_have_card(user_id, have_card)


async def update_user_show_variations(_: CallbackQuery, button: Button, manager: DialogManager) -> None:
    user_id = manager.event.from_user.id
    show_variations = int(button.widget_id)
    manager.middleware_data['user_show_variations'] = show_variations
    await update_show_variations(user_id, show_variations)


async def update_user_send_notifications(_: CallbackQuery, button: Button, manager: DialogManager) -> None:
    user_id = manager.event.from_user.id
    send_notifications = int(button.widget_id)
    manager.middleware_data['user_send_notifications'] = send_notifications
    await update_send_notifications(user_id, send_notifications)
