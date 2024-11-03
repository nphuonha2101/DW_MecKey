from enum import Enum

class EventType(Enum):
    SERVICE_NOTIFY_PROGRESS = 'service_notify_progress'
    SERVICE_NOTIFY_LOG = 'service_notify_log'
    GUI_NOTIFY = 'gui_notify'