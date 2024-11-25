import enum


class UserRole(enum.Enum):
    none = 0
    default = 1
    admin = 2


class UserShowVariations(enum.Enum):
    yes = 0
    no = 1
    only_cheaper = 2


class UserSendNotifications(enum.Enum):
    yes = 0
    no = 1
    only_lowering = 2

