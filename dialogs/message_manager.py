import ast
from typing import Union

from aiogram import Bot
from aiogram.types import InputFile, BufferedInputFile
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.manager.message_manager import MessageManager

from utils.graphs_generator import get_price_graph

GRAPH_URL_PREFIX = 'graph://'


class CustomMessageManager(MessageManager):
    async def get_media_source(self, media: MediaAttachment, bot: Bot) -> Union[InputFile, str]:
        if media.file_id:
            return await super().get_media_source(media, bot)
        if media.url and media.url.startswith(GRAPH_URL_PREFIX):
            product_id, product_title, have_card, middleware_data = media.url[len(GRAPH_URL_PREFIX):].split('~')

            product_id = int(product_id)
            have_card = have_card == 'True'
            middleware_data = ast.literal_eval(middleware_data)

            return BufferedInputFile(await get_price_graph(product_id, product_title, have_card, middleware_data),
                                     f'{product_id}.png')
        return await super().get_media_source(media, bot)