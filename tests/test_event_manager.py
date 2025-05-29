import pytest
import pygame
from src.event_manager import EventManager

@pytest.fixture
def event_manager():
    return EventManager()

def test_register_and_notify_listener(event_manager):
    called = []

    def listener(arg):
        called.append(arg)

    event_manager.register_listener('test_event', listener)
    event_manager.notify('test_event', 123)
    assert called == [123]

def test_unregister_listener(event_manager):
    called = []

    def listener(arg):
        called.append(arg)

    event_manager.register_listener('test_event', listener)
    event_manager.unregister_listener('test_event', listener)
    event_manager.notify('test_event', 456)
    assert called == []

def test_notify_multiple_listeners(event_manager):
    called = []

    def listener1(arg):
        called.append(('l1', arg))

    def listener2(arg):
        called.append(('l2', arg))

    event_manager.register_listener('test_event', listener1)
    event_manager.register_listener('test_event', listener2)
    event_manager.notify('test_event', 789)
    assert ('l1', 789) in called
    assert ('l2', 789) in called

def test_handle_event_calls_listener(event_manager):
    called = []

    def listener(event):
        called.append(event)

    pygame.init()
    event_type = pygame.USEREVENT + 1
    event_manager.register_listener(event_type, listener)
    event = pygame.event.Event(event_type, {})
    event_manager.handle_event(event)
    assert called and called[0].type == event_type
    pygame.quit()

def test_handle_event_ignores_unregistered(event_manager):
    pygame.init()
    event_type = pygame.USEREVENT + 2
    event = pygame.event.Event(event_type, {})
    # Nie rejestrujemy listenera
    # Sprawdzenie, że nie rzuca wyjątku
    event_manager.handle_event(event)
    pygame.quit()