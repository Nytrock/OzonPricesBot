from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from filters.user_role import IsUserNone
from states import states

router = Router()
router.message.filter(IsUserNone())


@router.message(CommandStart(), StateFilter(default_state))
async def registration_start(message: Message, i18n: dict[str, str], state: FSMContext):
    pass
