import os
import time

from injector import inject

from event.event import Event
from event.event_bus import EventBus
from event.event_level import EventLevel
from event.event_type import EventType
from gui.gui import GUI
from app_module.injector_init import injector
from services.transform.transform import Transform


class Controller:
    @inject
    def __init__(self, event_bus: EventBus, gui: GUI, is_auto: bool):
        self.event_bus = event_bus
        self.event_bus.subscribe(EventType.SERVICE_NOTIFY_PROGRESS, self.notify_progress_to_ui)
        self.event_bus.subscribe(EventType.SERVICE_NOTIFY_LOG, self.notify_log_to_ui)
        if not is_auto:
            self.event_bus.subscribe(EventType.GUI_NOTIFY, self.handle_gui_event)
        self.gui = gui

    def handle_gui_event(self, event: Event):
        if event.event_level == EventLevel.BUTTON_CLICK:
            self.begin_process(event.data)

    def begin_process(self, event_data: dict):
        transform = injector.get(Transform)
        if event_data["process_name"] == "akko_transform":


            status = event_data.get("status", None)
            file_path = event_data.get("file_path", None)

            if status is None or file_path is None:
                transform.set_feed_key("akko_feed")
                transform.run()
                return
            transform.run(status, file_path)

        elif event_data["process_name"] == "cps_transform":

            status = event_data.get("status", None)
            file_path = event_data.get("file_path", None)

            if status is None or file_path is None:
                transform.set_feed_key("cps_feed")
                transform.run()
                return

            transform.run(status, file_path)

    def notify_progress_to_ui(self, event: Event):
        self.gui.update_progress(event.event_level, event.data)

    def notify_log_to_ui(self, event: Event):
        self.gui.update_log(event.event_level, event.data)
