from injector import Module, provider, singleton

from db.db_manager import DatabaseManager   

from gui.gui import GUI
from event.event_bus import EventBus
from services.extract.akko_extract import AkkoExtract
from services.extract.cps_extract import CellphoneSExtract


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
    def provider_akko_extract(self, event_bus: EventBus) -> AkkoExtract:
        return AkkoExtract(event_bus)
    
    @singleton
    @provider
    def provider_cps_extract(self, event_bus: EventBus) -> CellphoneSExtract:
        return CellphoneSExtract(event_bus)
