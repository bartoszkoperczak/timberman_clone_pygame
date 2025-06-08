import pygame
import src.DEFAULTS as DEFAULTS
from src.interfaces.Drawable import Drawable
from src.interfaces.EventSubscriber import EventSubscriber
from src.assets_manager import assets
from src.event_manager import event_manager
from src.components.button import Button
from src.enums.GameMode import GameMode

OVERLAY_COLOR = (50, 50, 50, 180)
SCORE_COLOR = (255, 255, 255)

class HUD(Drawable, EventSubscriber):
    def __init__(self, game, mode: GameMode):
        self.game = game
        self.mode = mode
        self.return_button = Button(10, 10, assets.get("return_button"), self.return_to_menu)
        # Poprawiona ścieżka do fontu (bez ukośnika na początku)
        self.font = pygame.font.Font("assets/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", 48)
        self.lost_primary = False
        self.lost_secondary = False
        event_manager.register_listener(pygame.MOUSEBUTTONDOWN, self.handle_mouse_event)

    def draw(self, screen, time_str, time_over, score_primary=None, score_secondary=None):
        self._draw_scores(screen, score_primary, score_secondary)
        self._draw_timer(screen, time_str)
        if time_over and self.mode in (GameMode.MULTI_PLAYER, GameMode.VS_BOT):
            self._draw_time_over_overlay(screen, score_primary, score_secondary)
        self._draw_loss_overlay(screen)
        self.return_button.draw(screen)

    def _draw_scores(self, screen, score_primary, score_secondary):
        if self.mode == GameMode.SINGLE_PLAYER:
            score_text = self.font.render(str(score_primary), True, SCORE_COLOR)
            score_rect = score_text.get_rect(center=(DEFAULTS.VIRTUAL_WIDTH // 2, 30))
            screen.blit(score_text, score_rect)
        else:
            score_text_1 = self.font.render(str(score_primary), True, SCORE_COLOR)
            score_rect_1 = score_text_1.get_rect(center=(DEFAULTS.VIRTUAL_WIDTH // 4, 30))
            screen.blit(score_text_1, score_rect_1)

            score_text_2 = self.font.render(str(score_secondary), True, SCORE_COLOR)
            score_rect_2 = score_text_2.get_rect(center=(3 * DEFAULTS.VIRTUAL_WIDTH // 4, 30))
            screen.blit(score_text_2, score_rect_2)

    def _draw_timer(self, screen, time_str):
        timer_text = self.font.render(time_str, True, (200, 200, 200))
        timer_rect = timer_text.get_rect(center=(DEFAULTS.VIRTUAL_WIDTH // 2, 70))
        screen.blit(timer_text, timer_rect)

    def _draw_loss_overlay(self, screen):
        overlay = pygame.Surface((DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_HEIGHT), pygame.SRCALPHA)
        font_big = pygame.font.SysFont(None, 72)
        text = font_big.render("You've lost!", True, (255, 255, 255))

        if self.mode == GameMode.SINGLE_PLAYER and self.lost_primary:
            overlay.fill(OVERLAY_COLOR)
            screen.blit(overlay, (0, 0))
            screen.blit(text, text.get_rect(center=(DEFAULTS.VIRTUAL_WIDTH // 2, DEFAULTS.VIRTUAL_HEIGHT // 2)))
        elif self.mode in (GameMode.MULTI_PLAYER, GameMode.VS_BOT):
            if self.lost_primary:
                overlay_part = pygame.Surface((DEFAULTS.VIRTUAL_WIDTH // 2, DEFAULTS.VIRTUAL_HEIGHT), pygame.SRCALPHA)
                overlay_part.fill(OVERLAY_COLOR)
                screen.blit(overlay_part, (0, 0))
                screen.blit(text, text.get_rect(center=(DEFAULTS.VIRTUAL_WIDTH // 4, DEFAULTS.VIRTUAL_HEIGHT // 2)))
            if self.lost_secondary:
                overlay_part = pygame.Surface((DEFAULTS.VIRTUAL_WIDTH // 2, DEFAULTS.VIRTUAL_HEIGHT), pygame.SRCALPHA)
                overlay_part.fill(OVERLAY_COLOR)
                screen.blit(overlay_part, (DEFAULTS.VIRTUAL_WIDTH // 2, 0))
                screen.blit(text, text.get_rect(center=(3 * DEFAULTS.VIRTUAL_WIDTH // 4, DEFAULTS.VIRTUAL_HEIGHT // 2)))

    def _draw_time_over_overlay(self, screen, score_primary, score_secondary):
        overlay = pygame.Surface((DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        font_big = pygame.font.SysFont(None, 72)
        winner_img = None
        text = None
        if score_primary is not None and score_secondary is not None:
            if score_primary > score_secondary:
                text = font_big.render("Player 1 wins!", True, (255, 255, 255))
                winner_img = assets.get("character_red_straight_pose")
            elif score_primary < score_secondary:
                text = font_big.render("Player 2 wins!", True, (255, 255, 255))
                winner_img = assets.get('character_green_straight_pose')
            else:
                text = font_big.render("Draw!", True, (255, 255, 255))
        screen.blit(overlay, (0, 0))
        if text is not None:
            screen.blit(text, text.get_rect(center=(DEFAULTS.VIRTUAL_WIDTH // 2, DEFAULTS.VIRTUAL_HEIGHT // 2 - 60)))
        if winner_img is not None:
            winner_img = pygame.transform.scale(winner_img, (DEFAULTS.SPRITE_SIZE[0] * 2, DEFAULTS.SPRITE_SIZE[1] * 2))
            img_rect = winner_img.get_rect(center=(DEFAULTS.VIRTUAL_WIDTH // 2, DEFAULTS.VIRTUAL_HEIGHT // 2 + 60))
            screen.blit(winner_img, img_rect)

    def handle_mouse_event(self, event):
        self.return_button.handle_mouse_click(event)

    def unregister(self):
        event_manager.unregister_listener(pygame.MOUSEBUTTONDOWN, self.handle_mouse_event)

    def cleanup(self):
        self.unregister()

    def return_to_menu(self):
        from src.ui_manager import UIManager
        from src.view_manager import view_manager
        from src.game_window import game_window
        ui_manager = UIManager(game_window, view_manager)
        view_manager.change_view(ui_manager)

        self.game.save_game_history()