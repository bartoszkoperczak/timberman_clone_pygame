from datetime import datetime
from enum import Enum

from src.Drawable import Drawable
from src.game.GameEngine import GameEngine, SteeringMode


class GameMode(Enum):
    SINGLE_PLAYER = 1
    MULTI_PLAYER = 2
    VS_BOT = 3

class Game(Drawable):
    def __init__(self, mode: GameMode):
        self.mode = mode
        self.start_time = datetime.now()
        self.engines = {}

        if mode == GameMode.SINGLE_PLAYER:
            self.engines['primary'] = GameEngine(SteeringMode.PLAYER_1, self.get_callback('primary'))
        elif mode == GameMode.MULTI_PLAYER:
            self.engines['primary'] = GameEngine(SteeringMode.PLAYER_1, self.get_callback('primary'))
            self.engines['secondary'] = GameEngine(SteeringMode.PLAYER_2, self.get_callback('secondary'))
        elif mode == GameMode.VS_BOT:
            self.engines['primary'] = GameEngine(SteeringMode.PLAYER_1, self.get_callback('primary'))
            self.engines['secondary'] = GameEngine(SteeringMode.BOT, self.get_callback('secondary'))

    def get_callback(self, source):
        def callback(k, v):
            self.parse_engine_data(k, v, source)

        return callback

    def parse_engine_data(self, k, data, source):
        pass

    def draw(self, screen):
        for engine in self.engines.values():
            engine.draw(screen)

