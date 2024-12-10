class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, subscriber):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(subscriber)

    def publish(self, event_type, message):
        if event_type in self.subscribers:
            for subscriber in self.subscribers[event_type]:
                subscriber(message)