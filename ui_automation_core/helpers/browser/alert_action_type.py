from enum import Enum, auto


class AlertActionType(Enum):
    ACCEPT = auto()
    DISMISS = auto()