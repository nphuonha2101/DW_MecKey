from injector import Module, provider

from db.db_manager import DatabaseManager
from event.event_bus import EventBus


class AppModule(Module):
    @provider
    def provider_database_manager(self) -> DatabaseManager:
        return DatabaseManager()

    @provider
    def provider_event_bus(self) -> EventBus:
        return EventBus()