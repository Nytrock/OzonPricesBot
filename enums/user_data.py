import enum


# Роль пользователя
class UserRole(enum.Enum):
    none = 0
    default = 1
    admin = 2


# Настройка отображения вариантов
class UserShowVariations(enum.Enum):
    all = 0
    only_cheaper = 1


# Настройка отправки уведомлений
class UserSendNotifications(enum.Enum):
    yes = 0
    no = 1
    only_lowering = 2

