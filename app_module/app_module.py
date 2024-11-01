from injector import Module, provider, singleton

from controller.controller import Controller
from db.db_manager import DatabaseManager
from event.event_bus import EventBus
from gui.gui import GUI
from services.extract.akko_extract import AkkoExtract


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
    def provider_controller(self, event_bus: EventBus, gui: GUI) -> Controller:
        return Controller(event_bus, gui)

    @singleton
    @provider
    def provider_akko_extract(self, database_manager: DatabaseManager) -> AkkoExtract:
        return AkkoExtract(database_manager)