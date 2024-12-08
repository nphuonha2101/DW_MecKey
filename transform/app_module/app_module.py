from injector import Module, provider, singleton

from gui.gui import GUI
from event.event_bus import EventBus
from services.transform.transform import Transform


class AppModule(Module):

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
    def provider_transform(self, event_bus: EventBus) -> Transform:
        return Transform(event_bus)
