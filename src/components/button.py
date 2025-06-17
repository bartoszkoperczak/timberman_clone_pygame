import pygame
from src import DEFAULTS
from src.interfaces.EventSubscriber import EventSubscriber
from src.event_manager import event_manager

class Button(EventSubscriber):
    def __init__(self, x, y, image, callback):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.callback = callback
        self.hovered = False

        event_manager.register_listener(pygame.MOUSEBUTTONDOWN, self.handle_event)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        scaled_x = mouse_pos[0] * DEFAULTS.SCALE
        scaled_y = mouse_pos[1] * DEFAULTS.SCALE
        self.hovered = self.rect.collidepoint((scaled_x, scaled_y))

        if self.hovered:
            highlight = self.image.copy()
            highlight.fill((50, 50, 50, 60), special_flags=pygame.BLEND_RGBA_ADD)
            surface.blit(highlight, self.rect)
            pygame.draw.rect(surface, (255, 255, 0), self.rect, 3)
        else:
            surface.blit(self.image, self.rect)

    def handle_mouse_click(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if event.button != 1:
            return

        scaled_x = event.pos[0] * DEFAULTS.SCALE
        scaled_y = event.pos[1] * DEFAULTS.SCALE
        if self.rect.collidepoint((scaled_x, scaled_y)):
            self.callback()



    def handle_event(self, event):
        self.handle_mouse_click(event)

    def unregister(self):
        pass  # już nie rejestrujemy się globalnie
