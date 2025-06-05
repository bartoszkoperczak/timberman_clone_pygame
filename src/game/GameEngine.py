from enum import Enum
import pygame
from src.interfaces.Drawable import Drawable
from src.interfaces.EventSubscriber import EventSubscriber
from src.game.Character import Character
from src.game.Tree import Tree
import src.DEFAULTS as DEFAULTS
from src.event_manager import event_manager
import random

class SteeringMode(Enum):
    PLAYER_1 = 1
    PLAYER_2 = 2
    BOT = 3

class GameEngine(Drawable, EventSubscriber):
    def __init__(self, steering: SteeringMode, game_callback, rect):
        self.steering = steering
        self.game_callback = game_callback
        
        self.x_start, self.y_start = rect[0]
        self.x_end, self.y_end = rect[1]
        self.width = self.x_end - self.x_start
        self.height = self.y_end - self.y_start
        print(self.height)
        self.seed = random.randint(0, 255)

        self.character = Character(self.pos(self.width // 2 - DEFAULTS.SPRITE_SIZE[0] - DEFAULTS.TREE_SIZE[0] // 2, self.height - DEFAULTS.SPRITE_SIZE[1]), img_src='character_red' if steering == SteeringMode.PLAYER_1 else 'character_green')
        self.tree = Tree(self.pos(self.width // 2 - DEFAULTS.TREE_SIZE[0] // 2 , self.height - DEFAULTS.TREE_SIZE[1]))

        if steering != SteeringMode.BOT:
            self.steering = DEFAULTS.PLAYER_1_STEERING if steering == SteeringMode.PLAYER_1 else DEFAULTS.PLAYER_2_STEERING
            event_manager.register_listener(pygame.KEYDOWN, self.register_listener)

    def register_listener(self, e):
        # Blokada po przegranej
        if hasattr(self, 'lost') and self.lost:
            return
        if e.key == self.steering['left']:
            self.character.move(-1)
            self.check_collision()
        elif e.key == self.steering['right']:
            self.character.move(1)
            self.check_collision()
        elif e.key == self.steering['hit']:
            self.character.hit()
            self.tree.drop()
            self.game_callback("score", None)
            self.check_collision()

    def pos(self, x=0, y=0):
        return (self.x_start + x, self.y_start + y)

    def draw(self, screen):
        screen.fill((0, 128, self.seed), (self.x_start, self.y_start, self.width, self.height))
        self.character.draw(screen)
        self.tree.draw(screen)

    def cleanup(self):
        pass

    def unregister(self):
        if self.steering != SteeringMode.BOT:
            event_manager.unregister_listener(pygame.KEYDOWN, self.register_listener)
            
    def check_collision(self):
        # Sprawdź czy character jest na tej samej stronie co branch w najniższym logu
        lowest_log = self.tree.stack[-1]
        if lowest_log.branch_state != 0 and self.character.direction == lowest_log.branch_state:
            self.game_callback("lose", None)