from injector import Module, provider, singleton

from db.db_manager import DatabaseManager

from gui.gui import GUI
from event.event_bus import EventBus
from services.processing.processing import Processing


class AppModule(Module):

    @singleton
    @provider
    def provider_database_manager(self) -> DatabaseManager:
        return DatabaseManager()

    @singleton
    @provider
    def provider_event_bus(self) -> EventBus:
        return EventBus()

    @singleton
    @provider
    def provider_gui(self, event_bus: EventBus) -> GUI:
        return GUI(event_bus)

    @singleton
    @provider
    def provider_process(self, event_bus: EventBus) -> Processing:
        return Processing(event_bus)
