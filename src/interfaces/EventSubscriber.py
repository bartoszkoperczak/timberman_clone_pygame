from abc import ABC, abstractmethod

class EventSubscriber(ABC):
    @abstractmethod
    def unregister(self):
        pass