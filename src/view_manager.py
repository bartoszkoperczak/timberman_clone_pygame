from enum import Enum
import pygame

from src import DEFAULTS
from src.interfaces.Drawable import Drawable

class ViewState(Enum):
    MAIN_MENU = 1
    GAME = 2
    SETTINGS = 3
    GAME_OVER = 4

class ViewManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((DEFAULTS.WINDOW_WIDTH, DEFAULTS.WINDOW_HEIGHT))
        self.virtual_surface = pygame.Surface((DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_HEIGHT))
        self.current_view = None

    def change_view(self, new_view: Drawable):
        if self.current_view is not None:
            self.current_view.cleanup()
            
        self.current_view = new_view

    def draw(self):
        self.current_view.draw(self.virtual_surface)
        scaled_surface = pygame.transform.scale(self.virtual_surface, (DEFAULTS.WINDOW_WIDTH, DEFAULTS.WINDOW_HEIGHT))
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    def get_screen(self):
        return self.screen


view_manager = ViewManager()