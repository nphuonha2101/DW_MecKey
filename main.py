from app_module.app_module import AppModule
from injector import Injector

from event.event_bus import EventBus
from gui.gui import GUI

injector = Injector([AppModule])
event_bus = injector.get(EventBus)
gui = GUI(event_bus)

gui.create()
