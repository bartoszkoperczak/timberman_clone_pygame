import pygame
from random import randint
import src.DEFAULTS as DEFAULTS
from src.view_manager import view_manager
from src.assets_manager import assets
from src.interfaces.Drawable import Drawable
from src.game.GameEngine import GameEngine, SteeringMode
from src.game.HUD import HUD
from src.enums.GameMode import GameMode
from src.storage_service import storage_service

class Game(Drawable):
    def __init__(self, mode: GameMode, game_window=None):
        self.mode = mode
        self.game_window = game_window
        self.engines = {}

        background_index = randint(1, 5)
        self.background = pygame.transform.scale(assets.get(f"background{background_index}"), (DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_HEIGHT))
        # --- logika czasu ---
        self.time_limit = DEFAULTS.MULTIPLAYER_GAME_TIME if mode in (GameMode.MULTI_PLAYER, GameMode.VS_BOT) else None
        self.start_ticks = pygame.time.get_ticks()
        self.time_over = False
        self.elapsed_seconds = 0
        self.remaining_seconds = self.time_limit if self.time_limit else 0
        # ---
        self.hud = HUD(self, mode)
        self._init_engines()
        view_manager.change_view(self)

    def _init_engines(self):
        if self.mode == GameMode.SINGLE_PLAYER:
            self.engines['primary'] = GameEngine(SteeringMode.PLAYER_1, self.get_callback('primary'), rect=((0, 0), (DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_HEIGHT)))
        elif self.mode == GameMode.MULTI_PLAYER:
            self.engines['primary'] = GameEngine(SteeringMode.PLAYER_1, self.get_callback('primary'), rect=((0, 0), (0.5 * DEFAULTS.VIRTUAL_WIDTH , DEFAULTS.VIRTUAL_HEIGHT)))
            self.engines['secondary'] = GameEngine(SteeringMode.PLAYER_2, self.get_callback('secondary'), rect=((0.5 * DEFAULTS.VIRTUAL_WIDTH, 0), (DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_HEIGHT)))
        elif self.mode == GameMode.VS_BOT:
            self.engines['primary'] = GameEngine(SteeringMode.PLAYER_1, self.get_callback('primary'), rect=((0, 0), (0.5 * DEFAULTS.VIRTUAL_WIDTH , DEFAULTS.VIRTUAL_HEIGHT)))
            self.engines['secondary'] = GameEngine(SteeringMode.BOT, self.get_callback('secondary'), rect=((0.5 * DEFAULTS.VIRTUAL_WIDTH, 0), (DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_HEIGHT)))

    def get_callback(self, source):
        def callback(k, v):
            self.parse_engine_data(k, v, source)
        return callback

    def parse_engine_data(self, k, data, source):
        if k == "lose":
            self._handle_lose(source)

    def _handle_lose(self, source):
        self.engines[source].lost = True
        if source == "primary":
            self.hud.lost_primary = True
        elif source == "secondary":
            self.hud.lost_secondary = True

    def get_scores(self):
        primary = self.engines['primary'].score if 'primary' in self.engines else 0
        secondary = self.engines['secondary'].score if 'secondary' in self.engines else 0
        return primary, secondary

    def update_time(self):
        now_ticks = pygame.time.get_ticks()
        self.elapsed_seconds = (now_ticks - self.start_ticks) // 1000
        if self.mode == GameMode.SINGLE_PLAYER:
            pass  # czas liczy się do góry
        else:
            self.remaining_seconds = max(0, self.time_limit - self.elapsed_seconds)
            if self.remaining_seconds == 0:
                self.time_over = True

    def get_time_str(self):
        if self.mode == GameMode.SINGLE_PLAYER:
            total_seconds = self.elapsed_seconds
        else:
            total_seconds = self.remaining_seconds
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def _draw_background(self, screen):
        screen.blit(self.background, (0, 0))

    def save_game_history(self):
        primary, secondary = self.get_scores()
        game_record = {
            'mode': self.mode.value,
            'primary_score': primary,
            'secondary_score': secondary,
            'time_limit': self.time_limit or -1,
            'time': self.get_time_str()
        }
        storage_service.add_history_record(game_record)

    def draw(self, screen):
        self.update_time()
        self._draw_background(screen)
        for engine in self.engines.values():
            engine.draw(screen)
        primary, secondary = self.get_scores()
        self.hud.draw(screen, self.get_time_str(), self.time_over, primary, secondary)

    def cleanup(self):
        self.hud.cleanup()

