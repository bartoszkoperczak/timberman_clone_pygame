class EventManager:
    def __init__(self):
        self._listeners = {}
        self.loop_listeners = []

    def register_listener(self, event_type, listener):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def unregister_listener(self, event_type, listener):
        if event_type in self._listeners and listener in self._listeners[event_type]:
            self._listeners[event_type].remove(listener)

    def notify(self, event_type, *args):
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener(*args)

    def handle_event(self, event):
        if event.type in self._listeners:
            self.notify(event.type, event)

    def add_loop_listener(self, listener):
        if listener not in self.loop_listeners:
            self.loop_listeners.append(listener)

event_manager = EventManager()