from injector import inject

from event.event import Event
from event.event_bus import EventBus
from event.event_level import EventLevel
from event.event_type import EventType
from gui.gui import GUI


class Controller:
    @inject
    def __init__(self, event_bus: EventBus, gui: GUI):
        self.event_bus = event_bus
        self.event_bus.subscribe(EventType.SERVICE_NOTIFY, self.notify_ui)
        self.event_bus.subscribe(EventType.GUI_NOTIFY, self.handle_gui_event)
        self.gui = gui

    def notify_ui(self, event: Event):
        self.gui.update_progress(event.event_level, event.data)

    def handle_gui_event(self, event: Event):
        if event.event_level == EventLevel.BUTTON_CLICK:
            self.begin_process()

    def begin_process(self):
        pass