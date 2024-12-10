class Event:
    def __init__(self, event_level, data):
        self.event_level = event_level
        self.data = data

    def __str__(self):
        return f"Event type: {self.event_level}, data: {self.data}"