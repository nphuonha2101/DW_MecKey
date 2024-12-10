from injector import Module, provider, singleton

from db.db_manager import DatabaseManager

from gui.gui import GUI
from event.event_bus import EventBus
from services.load_to_warehouse.load_to_warehouse import LoadToWarehouse


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
    def provider_load_to_warehouse(self, database_manager: DatabaseManager, event_bus: EventBus) -> LoadToWarehouse:
        return LoadToWarehouse(database_manager, event_bus)
