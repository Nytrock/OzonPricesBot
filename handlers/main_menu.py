from aiogram import Router

from filters.user_role import IsUserRegistered

router = Router()
router.message.filter(IsUserRegistered())
