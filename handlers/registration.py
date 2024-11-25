from trace import Trace

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from database.methods import create_user
from filters.registration import RegistrationFilter
from filters.user_role import IsUserNone
from keyboards.keyboard_utils import create_reply_kb
from states.states import FSMRegistrationForm
from utils.registration_utils import is_message_yes, message_to_variations_enum, message_to_notifications_enum

router = Router()
router.message.filter(IsUserNone())


@router.message(CommandStart(), StateFilter(default_state))
async def registration_start_message(message: Message, i18n: dict[str, str]):
    await message.answer(
        text=i18n.get('registration-start')
    )

@router.message(Command('registrate'), StateFilter(default_state))
async def registration_command_message(message: Message, i18n: dict[str, str], state: FSMContext):
    await message.answer(text=i18n.get('registration-command'))

    await message.answer(
        text=i18n.get('registration-card'),
        reply_markup=create_reply_kb(i18n, 2, 'yes', 'no')
    )

    await state.update_data(id=message.from_user.id)
    await state.set_state(FSMRegistrationForm.fill_have_card)

@router.message(StateFilter(default_state))
async def registration_error_message(message: Message, i18n: dict[str, str]):
    await message.answer(
        text=i18n.get('registration-error')
    )


@router.message(StateFilter(FSMRegistrationForm.fill_have_card),
                RegistrationFilter(possible_replies=['yes', 'no']))
async def registration_card_success(message: Message, i18n: dict[str, str], state: FSMContext):
    await state.update_data(have_card=is_message_yes(message, i18n))

    await message.answer(
        text=i18n.get('registration-variation'),
        reply_markup=create_reply_kb(i18n, 2, 'yes', 'no', 'registration-variation-only-cheap')
    )
    await state.set_state(FSMRegistrationForm.fill_show_variations)


@router.message(StateFilter(FSMRegistrationForm.fill_have_card))
async def registration_card_error(message: Message, i18n: dict[str, str]):
    await message.answer(
        text=i18n.get('registration-card-error'),
        reply_markup=create_reply_kb(i18n, 2, 'yes', 'no')
    )


@router.message(StateFilter(FSMRegistrationForm.fill_show_variations),
                RegistrationFilter(possible_replies=['yes', 'no', 'registration-variation-only-cheap']))
async def registration_variations_success(message: Message, i18n: dict[str, str], state: FSMContext):
    await state.update_data(show_variations=message_to_variations_enum(message, i18n))

    await message.answer(
        text=i18n.get('registration-image'),
        reply_markup=create_reply_kb(i18n, 2, 'yes', 'no')
    )
    await state.set_state(FSMRegistrationForm.fill_show_product_image)


@router.message(StateFilter(FSMRegistrationForm.fill_show_variations))
async def registration_variations_error(message: Message, i18n: dict[str, str]):
    await message.answer(
        text=i18n.get('registration-variation-error'),
        reply_markup=create_reply_kb(i18n, 2, 'yes', 'no', 'registration-variation-only-cheap')
    )


@router.message(StateFilter(FSMRegistrationForm.fill_show_product_image),
                RegistrationFilter(possible_replies=['yes', 'no']))
async def registration_image_success(message: Message, i18n: dict[str, str], state: FSMContext):
    await state.update_data(show_product_image=is_message_yes(message, i18n))

    await message.answer(
        text=i18n.get('registration-notifications'),
        reply_markup=create_reply_kb(i18n, 2, 'yes', 'no', 'registration-notifications-only-lowering')
    )
    await state.set_state(FSMRegistrationForm.fill_send_notifications)


@router.message(StateFilter(FSMRegistrationForm.fill_show_product_image))
async def registration_image_error(message: Message, i18n: dict[str, str]):
    await message.answer(
        text=i18n.get('registration-image-error'),
        reply_markup=create_reply_kb(i18n, 2, 'yes', 'no')
    )


@router.message(StateFilter(FSMRegistrationForm.fill_send_notifications),
                RegistrationFilter(possible_replies=['yes', 'no', 'registration-notifications-only-lowering']))
async def registration_image_success(message: Message, i18n: dict[str, str], state: FSMContext):
    await state.update_data(send_notifications=message_to_notifications_enum(message, i18n))
    user_data = await state.get_data()
    await create_user(user_data)

    await message.answer(
        text=i18n.get('registration-finish'),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(StateFilter(FSMRegistrationForm.fill_send_notifications))
async def registration_image_error(message: Message, i18n: dict[str, str]):
    await message.answer(
        text=i18n.get('registration-notifications-error'),
        reply_markup=create_reply_kb(i18n, 2, 'yes', 'no', 'registration-notifications-only-lowering')
    )
