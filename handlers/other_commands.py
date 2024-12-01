from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from filters.registration import IsUserRegistered
from states.states import MainMenuDialogStates

router = Router()
router.message.filter(IsUserRegistered())


@router.message(CommandStart())
async def start_main_menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuDialogStates.main_menu, mode=StartMode.RESET_STACK)


@router.message(Command('registrate'))
async def registration_command_error(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n.get('registration_already_completed'))


@router.message(Command('help'))
async def registration_command_error(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n.get('help_command'))


@router.message()
async def random_message(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n.get('random_message'))
