from aiogram import Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager

from database.methods import create_user
from filters.registration import RegistrationFilter, IsUserRegistered
from handlers.other_commands import start_main_menu
from keyboards.keyboard_utils import create_reply_kb
from states.states import RegistrationStates
from utils.registration_utils import is_message_yes, message_to_variations_enum, message_to_notifications_enum

router = Router()
router.message.filter(~IsUserRegistered())


@router.message(CommandStart(), StateFilter(default_state))
async def registration_start_message(message: Message, i18n: dict[str, str]):
    await message.answer(
        text=i18n.get('registration_start')
    )


@router.message(Command('registrate'), StateFilter(default_state))
async def registration_command_message(message: Message, i18n: dict[str, str], state: FSMContext):
    await message.answer(text=i18n.get('registration_command'))

    await message.answer(
        text=i18n.get('registration_card'),
        reply_markup=create_reply_kb(i18n, 2, 'yes', 'no')
    )

    await state.update_data(id=message.from_user.id)
    await state.set_state(RegistrationStates.fill_have_card)


@router.message(StateFilter(default_state))
async def registration_error_message(message: Message, i18n: dict[str, str]):
    await message.answer(
        text=i18n.get('registration_error')
    )


@router.message(StateFilter(RegistrationStates.fill_have_card),
                RegistrationFilter(possible_replies=['yes', 'no']))
async def registration_card_success(message: Message, i18n: dict[str, str], state: FSMContext):
    await state.update_data(have_card=is_message_yes(message, i18n))

    await message.answer(
        text=i18n.get('registration_variation'),
        reply_markup=create_reply_kb(i18n, 2, 'UserShowVariations.all', 'UserShowVariations.only_cheaper')
    )
    await state.set_state(RegistrationStates.fill_show_variations)


@router.message(StateFilter(RegistrationStates.fill_have_card))
async def registration_card_error(message: Message, i18n: dict[str, str]):
    await message.answer(
        text=i18n.get('registration_card_error'),
        reply_markup=create_reply_kb(i18n, 2, 'yes', 'no')
    )


@router.message(StateFilter(RegistrationStates.fill_show_variations),
                RegistrationFilter(possible_replies=['UserShowVariations.all', 'UserShowVariations.only_cheaper']))
async def registration_variations_success(message: Message, i18n: dict[str, str], state: FSMContext):
    await state.update_data(show_variations=message_to_variations_enum(message, i18n))

    await message.answer(
        text=i18n.get('registration_notifications'),
        reply_markup=create_reply_kb(i18n, 2, 'yes', 'no', 'UserSendNotifications.only_lowering')
    )
    await state.set_state(RegistrationStates.fill_send_notifications)


@router.message(StateFilter(RegistrationStates.fill_show_variations))
async def registration_variations_error(message: Message, i18n: dict[str, str]):
    await message.answer(
        text=i18n.get('registration_variation_error'),
        reply_markup=create_reply_kb(i18n, 2, 'UserShowVariations.all', 'UserShowVariations.only_cheaper')
    )


@router.message(StateFilter(RegistrationStates.fill_send_notifications),
                RegistrationFilter(possible_replies=['yes', 'no', 'UserSendNotifications.only_lowering']))
async def registration_image_success(message: Message, i18n: dict[str, str], state: FSMContext, dialog_manager: DialogManager):
    await state.update_data(send_notifications=message_to_notifications_enum(message, i18n))
    user_data = await state.get_data()
    await create_user(user_data)

    await message.answer(
        text=i18n.get('registration_finish'),
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()
    await start_main_menu(message, dialog_manager)


@router.message(StateFilter(RegistrationStates.fill_send_notifications))
async def registration_image_error(message: Message, i18n: dict[str, str]):
    await message.answer(
        text=i18n.get('registration_notifications_error'),
        reply_markup=create_reply_kb(i18n, 2, 'yes', 'no', 'UserSendNotifications.only_lowering')
    )
