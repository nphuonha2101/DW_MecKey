from app_module.app_module import AppModule
from injector import Injector

from gui.gui import GUI

injector = Injector([AppModule])
gui = injector.get(GUI)

gui.create()
