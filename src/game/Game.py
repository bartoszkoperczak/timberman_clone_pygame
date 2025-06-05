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
        self.lost_primary = False
        self.lost_secondary = False

        event_manager.register_listener(pygame.MOUSEBUTTONDOWN, self.handle_mouse_event)

    def get_callback(self, source):
        def callback(k, v):
            self.parse_engine_data(k, v, source)

        return callback

    def parse_engine_data(self, k, data, source):
        if k in ("score", "log_cut"):
            if source == "primary":
                self.score_primary += 1
            elif source == "secondary":
                self.score_secondary += 1
        elif k == "lose":
            if source == "primary":
                self.lost_primary = True
                self.engines['primary'].lost = True
            elif source == "secondary":
                self.lost_secondary = True
                self.engines['secondary'].lost = True

    def return_to_menu(self):
        from src.ui_manager import UIManager
        from src.view_manager import view_manager
        ui_manager = UIManager(self.game_window, view_manager)
        view_manager.change_view(ui_manager)

    def draw(self, screen):
        for key, engine in self.engines.items():
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

        # Efekt przegranej
        overlay = pygame.Surface((DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_HEIGHT), pygame.SRCALPHA)
        font_big = pygame.font.SysFont(None, 72)
        text = font_big.render("You've lost!", True, (255, 255, 255))

        if self.mode == GameMode.SINGLE_PLAYER and self.lost_primary:
            overlay.fill((50, 50, 50, 180))
            screen.blit(overlay, (0, 0))
            screen.blit(text, text.get_rect(center=(DEFAULTS.VIRTUAL_WIDTH // 2, DEFAULTS.VIRTUAL_HEIGHT // 2)))
        elif self.mode in (GameMode.MULTI_PLAYER, GameMode.VS_BOT):
            if self.lost_primary:
                overlay_part = pygame.Surface((DEFAULTS.VIRTUAL_WIDTH // 2, DEFAULTS.VIRTUAL_HEIGHT), pygame.SRCALPHA)
                overlay_part.fill((50, 50, 50, 180))
                screen.blit(overlay_part, (0, 0))
                screen.blit(text, text.get_rect(center=(DEFAULTS.VIRTUAL_WIDTH // 4, DEFAULTS.VIRTUAL_HEIGHT // 2)))
            if self.lost_secondary:
                overlay_part = pygame.Surface((DEFAULTS.VIRTUAL_WIDTH // 2, DEFAULTS.VIRTUAL_HEIGHT), pygame.SRCALPHA)
                overlay_part.fill((50, 50, 50, 180))
                screen.blit(overlay_part, (DEFAULTS.VIRTUAL_WIDTH // 2, 0))
                screen.blit(text, text.get_rect(center=(3 * DEFAULTS.VIRTUAL_WIDTH // 4, DEFAULTS.VIRTUAL_HEIGHT // 2)))

    def cleanup(self):
        event_manager.unregister_listener(pygame.MOUSEBUTTONDOWN, self.handle_mouse_event)

    def handle_mouse_event(self, event):
        self.return_button.handle_mouse_click(event)