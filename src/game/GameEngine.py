from enum import Enum

class SteeringMode(Enum):
    PLAYER_1 = 1
    PLAYER_2 = 2
    BOT = 3

class GameEngine:
    def __init__(self, steering: SteeringMode, game_callback):
        pass