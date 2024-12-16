from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from filters.registration import IsUserRegistered
from states.states import MainMenuDialogStates

router = Router()
router.message.filter(IsUserRegistered())


# Запуск диалога
@router.message(CommandStart())
async def start_main_menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuDialogStates.main_menu, mode=StartMode.RESET_STACK)


# Команда регистрации (для уже зарегистрированных пользователей)
@router.message(Command('registrate'))
async def registration_command_error(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n.get('registration_already_completed'))


# Команда help
@router.message(Command('help'))
async def registration_command_error(message: Message, i18n: dict[str, str]):
    await message.answer(text=i18n.get('help_command'))
