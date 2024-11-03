from injector import Module, provider, singleton

from db.db_manager import DatabaseManager

from gui.gui import GUI
from event.event_bus import EventBus
from services.extract.akko_extract import AkkoExtract
from services.processing.akko_processing import AkkoProcessing


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
    def provider_akko_extract(self, database_manager: DatabaseManager, event_bus: EventBus) -> AkkoExtract:
        return AkkoExtract(database_manager, event_bus)

    @singleton
    @provider
    def provider_akko_process(self, database_manager: DatabaseManager, event_bus: EventBus) -> AkkoProcessing:
        return AkkoProcessing(database_manager, event_bus)