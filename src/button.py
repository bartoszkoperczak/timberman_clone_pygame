import pygame
from src import DEFAULTS
from src.EventSubscriber import EventSubscriber
from src.event_manager import event_manager


# poprawilem ze buttony same sobie rejestruja eventy

class Button(EventSubscriber):
    def __init__(self, x, y, image, callback):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.callback = callback
        event_manager.register_listener(pygame.MOUSEBUTTONDOWN, self.handle_mouse_click)

    def draw(self, surface):
        surface.fill((128, 0, 0), self.rect) # testing purpose, fill with red
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (0, 255, 0), self.rect, 2) # testing purpose, draw green border

    def handle_mouse_click(self, event):
        if event.button != 1:
            return

        scaled_x = event.pos[0] * DEFAULTS.SCALE
        scaled_y = event.pos[1] * DEFAULTS.SCALE
        if self.rect.collidepoint((scaled_x, scaled_y)):
            self.callback()

    def unregister(self):
        print(f"Unregistering listener for event type: {pygame.MOUSEBUTTONDOWN}")
        event_manager.unregister_listener(pygame.MOUSEBUTTONDOWN, self.handle_mouse_click)

    def __del__(self):
        self.unregister()