from datetime import datetime
from enum import Enum

from src.interfaces.Drawable import Drawable
from src.game.GameEngine import GameEngine, SteeringMode
from src.view_manager import view_manager
import src.DEFAULTS as DEFAULTS


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
            self.engines['primary'] = GameEngine(SteeringMode.PLAYER_1, self.get_callback('primary'), rect=((0, 0), (DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_HEIGHT)))
        elif mode == GameMode.MULTI_PLAYER:
            self.engines['primary'] = GameEngine(SteeringMode.PLAYER_1, self.get_callback('primary'), rect=((0, 0), (0.5 * DEFAULTS.VIRTUAL_WIDTH , DEFAULTS.VIRTUAL_HEIGHT)))
            self.engines['secondary'] = GameEngine(SteeringMode.PLAYER_2, self.get_callback('secondary'), rect=((0.5 * DEFAULTS.VIRTUAL_WIDTH, 0), (DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_HEIGHT)))
        elif mode == GameMode.VS_BOT:
            self.engines['primary'] = GameEngine(SteeringMode.PLAYER_1, self.get_callback('primary'), rect=((0, 0), (0.5 * DEFAULTS.VIRTUAL_WIDTH , DEFAULTS.VIRTUAL_HEIGHT)))
            self.engines['secondary'] = GameEngine(SteeringMode.BOT, self.get_callback('secondary'), rect=((0.5 * DEFAULTS.VIRTUAL_WIDTH, 0), (DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_WIDTH)))

        view_manager.change_view(self)

    def get_callback(self, source):
        def callback(k, v):
            self.parse_engine_data(k, v, source)

        return callback

    def parse_engine_data(self, k, data, source):
        pass

    def draw(self, screen):
        for engine in self.engines.values():
            engine.draw(screen)

    def cleanup(self):
        pass