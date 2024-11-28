from typing import Any
from pyrogram import Client

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from pyrogram.errors import UsernameInvalid

from config_data.config import load_config
from database.methods import get_all_users, get_all_products, get_all_sellers, make_user_admin


async def get_admin_statistic(**kwargs) -> dict[str, Any]:
    data = {}

    data['users_count'] = len(await get_all_users())
    data['products_count'] = len(await get_all_products())
    data['sellers_count'] = len(await get_all_sellers())

    return data


async def add_new_admin(message: Message, _: MessageInput, manager: DialogManager):
    config = load_config().tg_api
    async with Client(config.username, api_id=config.api_id, api_hash=config.api_hash) as ubot:
        try:
            user = await ubot.get_users(message.text)
            await make_user_admin(user.id)
            await message.answer(manager.middleware_data['i18n']['admin_added'])
            await manager.done()
        except UsernameInvalid:
            await message.answer(manager.middleware_data['i18n']['admin_add_error'])
