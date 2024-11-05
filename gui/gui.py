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
    root.geometry(f"{width}x{height}+{x}+{y-50}")


def create_text_area(root):
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=25)
    text_area.config(state=tk.DISABLED)

    text_area.pack()
    return text_area


def button_style():
    return {
        "width": 15,
        "height": 2,
        "bg": "#4CAF50",
        "fg": "white",
        "font": ('Arial', 10, 'bold'),
        "relief": tk.FLAT,
        "borderwidth": 0,
        "cursor": "hand2",
    }


def _update_text_area(event_type, data, text_area=None):
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, f"{data}\n")  # Sử dụng data thay cho message nếu cần

    if  event_type == EventLevel.ERROR:
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
        self.text_area_log = None
        self.text_area_progress = None
        self.button_frame = None
        self.event_bus = event_bus


    def create(self):
        root = tk.Tk()
        root.title("Tool")
        center_window(root, 700, 500)

        notebook = ttk.Notebook(root)
        notebook.pack(expand=1, fill='both')

        # Progress tab
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text='Progress')
        self.text_area_progress = create_text_area(tab1)
        self.button_frame = self.create_button_frame(tab1)

        # Log tab
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text='Log')
        self.text_area_log = create_text_area(tab2)

        root.mainloop()


    def create_button_frame(self, root):
        button_frame = tk.Frame(root)
        button_frame.pack(padx=20, pady=20)

        akko_button = tk.Button(button_frame, text="Scrape Akko".upper(), command=lambda: self.on_button_click(akko_button), **button_style())
        akko_button.pack()
        return button_frame

    def on_button_click(self, button):
        button.config(state=tk.DISABLED)
        self.update_progress(EventLevel.INFO, "Running scrape...")
        thread = threading.Thread(target=lambda: self.event_bus.publish(EventType.GUI_NOTIFY, Event(EventLevel.BUTTON_CLICK, None)))
        thread.start()


    def update_progress(self, event_type, data):
        data = f"[{event_type}] {datetime.now()}: {data}"
        _update_text_area(event_type, data, self.text_area_progress)

    def update_log(self, event_type, data):
        data = f"[{event_type}] {datetime.now()}: {data}"
        _update_text_area(event_type, data, self.text_area_log)

