import pygame
import pytest
from src.event_manager import EventManager

@pytest.fixture
def event_manager():
    return EventManager()

def test_listener_called_on_pygame_keydown(event_manager):
    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    called = {}

    def listener(key):
        called['key'] = key

    event_manager.register_listener('keydown', listener)

    key_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
    pygame.event.post(key_event)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            event_manager.notify('keydown', event.key)

    assert called['key'] == pygame.K_SPACE

    pygame.quit()