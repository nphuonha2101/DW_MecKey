from enum import Enum

class EventLevel(Enum):
    SUCCESS = 'success'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'
    BUTTON_CLICK = 'button_click'