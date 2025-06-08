from src.interfaces.Drawable import Drawable
from abc import abstractmethod

class Obstacle(Drawable):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def collide_rect(self, other_rect):
        pass

    @abstractmethod
    def update(self):
        pass
