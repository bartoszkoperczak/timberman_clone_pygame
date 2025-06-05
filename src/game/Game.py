from datetime import datetime
from enum import Enum

from src.interfaces.Drawable import Drawable
from src.game.GameEngine import GameEngine, SteeringMode
from src.view_manager import view_manager
import src.DEFAULTS as DEFAULTS
import pygame
from src.assets_manager import assets
from src.event_manager import event_manager
from src.components.button import Button


class GameMode(Enum):
    SINGLE_PLAYER = 1
    MULTI_PLAYER = 2
    VS_BOT = 3

class Game(Drawable):
    def __init__(self, mode: GameMode, game_window=None):
        self.mode = mode
        self.start_time = datetime.now()
        self.engines = {}
        self.game_window = game_window

        if mode == GameMode.SINGLE_PLAYER:
            self.engines['primary'] = GameEngine(SteeringMode.PLAYER_1, self.get_callback('primary'), rect=((0, 0), (DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_HEIGHT)))
        elif mode == GameMode.MULTI_PLAYER:
            self.engines['primary'] = GameEngine(SteeringMode.PLAYER_1, self.get_callback('primary'), rect=((0, 0), (0.5 * DEFAULTS.VIRTUAL_WIDTH , DEFAULTS.VIRTUAL_HEIGHT)))
            self.engines['secondary'] = GameEngine(SteeringMode.PLAYER_2, self.get_callback('secondary'), rect=((0.5 * DEFAULTS.VIRTUAL_WIDTH, 0), (DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_HEIGHT)))
        elif mode == GameMode.VS_BOT:
            self.engines['primary'] = GameEngine(SteeringMode.PLAYER_1, self.get_callback('primary'), rect=((0, 0), (0.5 * DEFAULTS.VIRTUAL_WIDTH , DEFAULTS.VIRTUAL_HEIGHT)))
            self.engines['secondary'] = GameEngine(SteeringMode.BOT, self.get_callback('secondary'), rect=((0.5 * DEFAULTS.VIRTUAL_WIDTH, 0), (DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_WIDTH)))

        view_manager.change_view(self)
        self.return_button = Button(10, 10, assets.get("return_button"), self.return_to_menu)
        self.font = pygame.font.SysFont(None, 48)
        self.score_primary = 0
        self.score_secondary = 0

        event_manager.register_listener(pygame.MOUSEBUTTONDOWN, self.handle_mouse_event)

    def get_callback(self, source):
        def callback(k, v):
            self.parse_engine_data(k, v, source)

        return callback

    def parse_engine_data(self, k, data, source):
        # Przykład: k == "score" lub k == "log_cut"
        if k in ("score", "log_cut"):
            if source == "primary":
                self.score_primary += 1
            elif source == "secondary":
                self.score_secondary += 1

    def return_to_menu(self):
        from src.ui_manager import UIManager
        from src.view_manager import view_manager
        ui_manager = UIManager(self.game_window, view_manager)
        view_manager.change_view(ui_manager)

    def draw(self, screen):
        for engine in self.engines.values():
            engine.draw(screen)
        self.return_button.draw(screen)

        if self.mode == GameMode.SINGLE_PLAYER:
            # Jeden licznik na środku
            score_text = self.font.render(str(self.score_primary), True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(DEFAULTS.VIRTUAL_WIDTH // 2, 30))
            screen.blit(score_text, score_rect)
        else:
            # Dwa liczniki na środku każdej połowy
            score_text_1 = self.font.render(str(self.score_primary), True, (255, 255, 255))
            score_rect_1 = score_text_1.get_rect(center=(DEFAULTS.VIRTUAL_WIDTH // 4, 30))
            screen.blit(score_text_1, score_rect_1)

            score_text_2 = self.font.render(str(self.score_secondary), True, (255, 255, 255))
            score_rect_2 = score_text_2.get_rect(center=(3 * DEFAULTS.VIRTUAL_WIDTH // 4, 30))
            screen.blit(score_text_2, score_rect_2)

    def cleanup(self):
        event_manager.unregister_listener(pygame.MOUSEBUTTONDOWN, self.handle_mouse_event)

    def handle_mouse_event(self, event):
        self.return_button.handle_mouse_click(event)