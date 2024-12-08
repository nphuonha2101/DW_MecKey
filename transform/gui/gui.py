import threading
import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext, Event, ttk
from dotenv import load_dotenv

from event.event_bus import EventBus
from event.event_level import EventLevel
from event.event import Event
from event.event_type import EventType

load_dotenv()


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y - 50}")


def create_text_area(root):
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=25)
    text_area.config(state=tk.DISABLED)

    text_area.pack()
    return text_area


def create_text_area_with_input_and_select(parent):
    frame = tk.Frame(parent)
    frame.pack(expand=1, fill='both')

    text_area = tk.Text(frame, wrap='word')
    text_area.pack(expand=1, fill='both')

    input_frame = tk.Frame(frame)
    input_frame.pack(fill='x', pady=5)

    input_field = tk.Entry(input_frame)
    input_field.pack(side='left', fill='x', expand=True, padx=(0, 5))

    options = ["RT", "TX", "ST", "FT"]
    selected_option = tk.StringVar(input_frame)
    selected_option.set(options[0])

    option_menu = tk.OptionMenu(input_frame, selected_option, *options)
    option_menu.pack(side='left')

    return frame, text_area, input_field, selected_option


def button_style():
    return {
        "width": 30,
        "height": 2,
        "bg": "#4CAF50",
        "fg": "white",
        "font": ('Segoe UI', 10, 'bold'),
        "relief": tk.FLAT,
        "borderwidth": 0,
        "cursor": "hand2",
    }


def _update_text_area(event_type, data, text_area=None):
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, f"{data}\n")

    if event_type == EventLevel.ERROR:
        text_area.tag_add("error", "1.0", "end")
        text_area.tag_config("error", foreground="red")
    elif event_type == EventLevel.SUCCESS:
        text_area.tag_add("success", "1.0", "end")
        text_area.tag_config("success", foreground="green")
    elif event_type == EventLevel.WARNING:
        text_area.tag_add("warning", "1.0", "end")
        text_area.tag_config("warning", foreground="orange")
    elif event_type == EventLevel.INFO:
        text_area.tag_add("info", "1.0", "end")
        text_area.tag_config("info", foreground="blue")
    text_area.config(state=tk.DISABLED)


class GUI:
    def __init__(self, event_bus: EventBus):
        self.root = None
        self.status_options = None
        self.file_path_input = None
        self.text_area_log = None
        self.text_area_progress = None
        self.input_field_progress = None
        self.selected_option_progress = None
        self.button_frame = None
        self.event_bus = event_bus

    def create(self):
        self.root = tk.Tk()
        self.root.title("Tool")
        center_window(self.root, 700, 550)

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=1, fill='both')

        # Progress tab
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text='Progress')

        # Create text area with input and select option
        progress_frame, self.text_area_progress, self.file_path_input, self.status_options = create_text_area_with_input_and_select(
            tab1)

        # Create button frame
        self.button_frame = self.create_button_frame(tab1)

        # Pack frames in the desired order
        progress_frame.pack(expand=1, fill='both')
        self.button_frame.pack(pady=10)

        # Log tab
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text='Log')
        self.text_area_log = create_text_area(tab2)

    def loop(self):
        self.root.mainloop()

    def create_button_frame(self, root):
        button_frame = tk.Frame(root)
        button_frame.pack(padx=20, pady=20)

        akko_button = tk.Button(button_frame, text="Transform Akko".upper(),
                                command=lambda: self.on_button_click("akko_transform"), **button_style())
        akko_button.grid(row=0, column=0, padx=5)

        cps_button = tk.Button(button_frame, text="Transform CellphoneS".upper(),
                               command=lambda: self.on_button_click("cps_transform"), **button_style())
        cps_button.grid(row=0, column=1, padx=5)

        return button_frame

    def on_button_click(self, process_name):
        thread = threading.Thread(target=lambda: self.event_bus.publish(
            EventType.GUI_NOTIFY, Event(EventLevel.BUTTON_CLICK,
                                        {
                                            "process_name": process_name,
                                            "status": self.status_options.get(),
                                            "file_path": self.file_path_input.get()
                                        })))
        thread.start()

    def update_progress(self, event_type, data):
        data = f"[{event_type}] {datetime.now()}: {data}"
        _update_text_area(event_type, data, self.text_area_progress)

    def update_log(self, event_type, data):
        data = f"[{event_type}] {datetime.now()}: {data}"
        _update_text_area(event_type, data, self.text_area_log)
