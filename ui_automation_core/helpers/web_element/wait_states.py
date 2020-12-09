from enum import Enum


class ElementWaitState(Enum):
    """
    An explicit wait can be applied to the condition that tries to find the web element in question.
    If the condition finds the element, it returns the element or a boolean value as the result.
    If not, the wait command tries the condition again after a short delay.\n
    USAGE: ElementWaitState.PRESENT
    """
    PRESENT = 1
    VISIBLE = 2
    INVISIBLE = 3
    CLICKABLE = 4
    SELECTED = 5
    FRAME_AVAILABLE_AND_SWITCH_TO = 6
    PRESENT_OF_ALL = 7
    VISIBLE_OF_ALL = 8
    VISIBLE_OF_ANY = 9
