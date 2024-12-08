from controller.controller import Controller
from event.event_bus import EventBus
from app_module.injector_init import injector
from gui.gui import GUI
import argparse


def main():
    is_auto = False

    parser = argparse.ArgumentParser(description='process param')
    parser.add_argument('--auto', action='store_true', help='auto mode')
    parser.add_argument('-pn', '--process_name', type=str, help='process name')

    args = parser.parse_args()

    event_bus = injector.get(EventBus)
    gui = injector.get(GUI)
    controller = Controller(event_bus, gui, is_auto)
    gui.create()

    if args.auto:
        is_auto = True
        if not args.process_name:
            print("Please enter process name")
            return
        controller.begin_process({"process_name": args.process_name})
    else:
        gui.loop()


if __name__ == '__main__':
    main()
