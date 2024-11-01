from app_module.app_module import AppModule
from injector import Injector

from controller.controller import Controller
from event.event_bus import EventBus

injector = Injector([AppModule])
controller = injector.get(Controller)  # Ensure Controller is instantiated
event_bus = injector.get(EventBus)
controller.gui.create()
print(event_bus.subscribers)  # Print subscribers after Controller is instantiated


