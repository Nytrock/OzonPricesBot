from aiogram import Router

from filters.user_role import IsUserAdmin

router = Router()
router.message.filter(IsUserAdmin())
