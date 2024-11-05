from controller.controller import Controller
from event.event_bus import EventBus
from app_module.injector_init import injector
from gui.gui import GUI


def main():
    event_bus = injector.get(EventBus)
    gui = injector.get(GUI)
    Controller(event_bus, gui)
    gui.create()

if __name__ == '__main__':
    main()



