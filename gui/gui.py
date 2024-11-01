import threading
import tkinter as tk
from tkinter import scrolledtext, Event

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


class GUI:
    def __init__(self, event_bus: EventBus):
        self.text_area = None
        self.button_frame = None
        self.event_bus = event_bus


    def create(self):
        root = tk.Tk()
        root.title("Tool")
        center_window(root, 700, 500)

        self.text_area = create_text_area(root)
        self.button_frame = self.create_button_frame(root)

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

    # def run_akko(self, button):
    #     self.process_manager.run_processes()
    #     button.config(state=tk.NORMAL)

    def update_progress(self, event_type, data):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"{data}\n")  # Sử dụng data thay cho message nếu cần

        if  event_type == EventLevel.ERROR:
            self.text_area.tag_add("error", "1.0", "end")
            self.text_area.tag_config("error", foreground="red")
        elif event_type == EventLevel.SUCCESS:
            self.text_area.tag_add("success", "1.0", "end")
            self.text_area.tag_config("success", foreground="green")
        elif event_type == EventLevel.WARNING:
            self.text_area.tag_add("warning", "1.0", "end")
            self.text_area.tag_config("warning", foreground="orange")
        elif event_type == EventLevel.INFO:
            self.text_area.tag_add("info", "1.0", "end")
            self.text_area.tag_config("info", foreground="blue")


        self.text_area.config(state=tk.DISABLED)

