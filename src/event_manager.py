class EventManager:
    def __init__(self):
        self._listeners = {}

    def register_listener(self, event_type, listener):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def unregister_listener(self, event_type, listener):
        if event_type in self._listeners and listener in self._listeners[event_type]:
            self._listeners[event_type].remove(listener)

    def notify(self, key_code):
        if key_code in self._listeners:
            for listener in self._listeners[key_code]:
                listener()

    def parse_keys(self, keys_pressed):
        for key_code, pressed in enumerate(keys_pressed):
            if pressed:
                self.notify(key_code)


event_manager = EventManager()