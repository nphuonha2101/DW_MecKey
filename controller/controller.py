from injector import inject

from event.event import Event
from event.event_bus import EventBus
from event.event_level import EventLevel
from event.event_type import EventType
from gui.gui import GUI
from app_module.injector_init import injector
from services.extract.akko_extract import AkkoExtract
from services.processing.akko_processing import AkkoProcessing


def begin_process():
    # akko_extract = injector.get(AkkoExtract)
    # akko_extract.run()

    akko_process = injector.get(AkkoProcessing)
    akko_process.run()


def handle_gui_event(event: Event):
    if event.event_level == EventLevel.BUTTON_CLICK:
        begin_process()


class Controller:
    @inject
    def __init__(self, event_bus: EventBus, gui: GUI):
        self.event_bus = event_bus
        self.event_bus.subscribe(EventType.SERVICE_NOTIFY_PROGRESS, self.notify_progress_to_ui)
        self.event_bus.subscribe(EventType.SERVICE_NOTIFY_LOG, self.notify_log_to_ui)
        self.event_bus.subscribe(EventType.GUI_NOTIFY, handle_gui_event)
        self.gui = gui

    def notify_progress_to_ui(self, event: Event):
        self.gui.update_progress(event.event_level, event.data)

    def notify_log_to_ui(self, event: Event):
        self.gui.update_log(event.event_level, event.data)

