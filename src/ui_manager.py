import pygame
import src.DEFAULTS as DEFAULTS
from src.assets_manager import assets
from src.interfaces.Drawable import Drawable
from src.components.button import Button
from src.storage_service import storage_service
from src.enums.GameMode import GameMode


class UIManager(Drawable):
    def __init__(self, game_window, view_manager):
        self.game_window = game_window
        self.view_manager = view_manager
        self.current_screen = 'main'
        self.background_img = pygame.transform.scale(
            assets.get("menu_background"),
            (DEFAULTS.VIRTUAL_WIDTH, DEFAULTS.VIRTUAL_HEIGHT)
        )
        self.buttons = []
        self.assets = self.load_assets()
        self.create_main_menu()
        self.music_volume = 0.3  # domyślna głośność
        self.slider_rect = pygame.Rect(395, 67, 170, 10)  # pozycja i rozmiar slidera
        self.slider_dragging = False

    def load_assets(self):
        return {
            'singleplayer': pygame.image.load('assets/ui/singleplayer_button.png'),
            'multiplayer': pygame.image.load('assets/ui/multiplayer_button.png'),
            'settings': pygame.image.load('assets/ui/settings.png'),
            'quit': pygame.image.load('assets/ui/quit_button.png'),
            'return': pygame.image.load('assets/ui/return_button.png'),
            '1vs1': pygame.image.load('assets/ui/1vs1_button.png'),
            '1vsbot': pygame.image.load('assets/ui/1vsbot_button.png'),
            'settings_button': pygame.image.load('assets/ui/settings_button.png'),
            'save_button': pygame.image.load('assets/ui/save_button.png'),
            'change_button': pygame.image.load('assets/ui/change_button.png')
        }

    def create_main_menu(self):
        """Create and display the main menu with navigation buttons."""
        print("Creating main menu")
        self.clear_buttons()
        self.buttons = [
            Button(400, 50, self.assets['singleplayer'], self.game_window.start_singleplayer),
            Button(400, 150, self.assets['multiplayer'], self.show_multiplayer_menu),
            Button(400, 300, self.assets['settings_button'], self.show_settings),
            Button(400, 450, self.assets['quit'], self.game_window.quit_game)
        ]
        self.current_screen = 'main'

    def show_multiplayer_menu(self):
        """Display the multiplayer menu with available multiplayer modes."""
        print("Creating multiplayer menu")
        self.clear_buttons()
        self.buttons = [
            Button(400, 50, self.assets['1vs1'], self.game_window.start_1vs1),
            Button(400, 200, self.assets['1vsbot'], self.game_window.start_1vsbot),
            Button(400, 350, self.assets['return'], self.create_main_menu),
        ]
        self.current_screen = 'multiplayer'

    def show_settings(self):
        """Display the settings menu, including controls and volume slider."""
        print("Creating settings menu")
        self.clear_buttons()
        self.buttons = [
            Button(30, DEFAULTS.VIRTUAL_HEIGHT - 70, self.assets['return'], self.create_main_menu),
            Button(DEFAULTS.VIRTUAL_WIDTH - 200, DEFAULTS.VIRTUAL_HEIGHT - 70, self.assets['save_button'], self.show_history)
        ]
        self.current_screen = 'settings'

    def clear_buttons(self):
        for button in self.buttons:
            button.unregister()
        self.buttons.clear()

    def quit_game(self):
        pygame.quit()
        exit()

    def draw(self, surface):
        """Draw the current UI screen and its elements on the given surface."""
        surface.blit(self.background_img, (0, 0))
        if self.current_screen == 'settings':
            self.draw_settings(surface)
        elif self.current_screen == 'history':
            self.draw_history(surface)
        else:
            self.draw_default(surface)
        for button in self.buttons:
            button.draw(surface)

    def draw_settings(self, surface):
        """Draw the settings screen, including controls and volume slider."""
        settings_img = self.assets['settings']
        scaled_settings = pygame.transform.scale(
            settings_img,
            (int(settings_img.get_width() * 1.5), int(settings_img.get_height() * 1.5))
        )
        img_x = 365
        img_y = 40
        surface.blit(scaled_settings, (img_x, img_y))
        font = pygame.font.SysFont(None, 32)
        controls = storage_service.get_controls()
        y1 = 210
        y2 = 360
        x_left = 100
        x_center = DEFAULTS.VIRTUAL_WIDTH // 2 - 80
        x_right = DEFAULTS.VIRTUAL_WIDTH - 250
        p1_label = font.render("Player 1:", True, (255,255,255))
        surface.blit(p1_label, (60, y1 - 60))
        l_txt = font.render(f"Lewo [{pygame.key.name(controls['player1']['left'])}]", True, (255,255,255))
        surface.blit(l_txt, (x_left, y1 - 40))
        h_txt = font.render(f"Cios [{pygame.key.name(controls['player1']['hit'])}]", True, (255,255,255))
        surface.blit(h_txt, (x_center, y1 - 40))
        r_txt = font.render(f"Prawo [{pygame.key.name(controls['player1']['right'])}]", True, (255,255,255))
        surface.blit(r_txt, (x_right, y1 - 40))
        p2_label = font.render("Player 2:", True, (255,255,255))
        surface.blit(p2_label, (60, y2 - 60))
        l2_txt = font.render(f"Lewo [{pygame.key.name(controls['player2']['left'])}]", True, (255,255,255))
        surface.blit(l2_txt, (x_left, y2 - 40))
        h2_txt = font.render(f"Cios [{pygame.key.name(controls['player2']['hit'])}]", True, (255,255,255))
        surface.blit(h2_txt, (x_center, y2 - 40))
        r2_txt = font.render(f"Prawo [{pygame.key.name(controls['player2']['right'])}]", True, (255,255,255))
        surface.blit(r2_txt, (x_right, y2 - 40))
        pygame.draw.rect(surface, (180, 180, 180), self.slider_rect)
        knob_x = self.slider_rect.x + int(self.music_volume * self.slider_rect.width)
        knob_rect = pygame.Rect(knob_x - 5, self.slider_rect.y - 4, 10, 18)
        pygame.draw.rect(surface, (80, 80, 255), knob_rect)
        if hasattr(self, "awaiting_key"):
            info = font.render("Naciśnij nowy klawisz...", True, (255, 200, 0))
            surface.blit(info, (380, 440))
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.get_change_buttons():
            img = self.assets['change_button'].copy()
            if btn["rect"].collidepoint(mouse_pos):
                img.fill((50, 50, 50, 60), special_flags=pygame.BLEND_RGBA_ADD)
                pygame.draw.rect(img, (255, 255, 0), img.get_rect(), 3)
            surface.blit(img, btn["rect"].topleft)

    def draw_history(self, surface):
        """Draw the game history screen with a list of previous games."""
        font = pygame.font.SysFont(None, 32)
        title = font.render('Game history:', True, (0,0,0))
        surface.blit(title, (60, 30))
        y = 120
        if hasattr(self, 'history_games') and self.history_games:
            for i, game in enumerate(self.history_games)[-10:]:
                mode = game.get('mode', '-')
                p1 = game.get('primary_score', '-')
                p2 = game.get('secondary_score', '-')
                time = game.get('time', '-')
                time_limit = game.get('time_limit', '-')
                timestamp = game.get('timestamp', '-')
                if mode == GameMode.SINGLE_PLAYER.value:
                    mode_str = 'Singleplayer'
                    time_str = f"Time: {time}"
                elif mode == GameMode.MULTI_PLAYER.value:
                    mode_str = '1vs1'
                    time_str = f"Time limit: {time_limit if time_limit != -1 else 'none'}"
                elif mode == GameMode.VS_BOT.value:
                    mode_str = 'vs Bot'
                    time_str = f"Time limit: {time_limit if time_limit != -1 else 'none'}"
                else:
                    mode_str = str(mode)
                    time_str = f"Time/limit: {time if time != '-' else time_limit}"
                desc = f"{i+1}. {mode_str} | Score: {p1} : {p2} | {time_str} | Date: {timestamp[:19].replace('T', ' ')}"
                txt = font.render(desc, True, (0,0,0))
                surface.blit(txt, (60, y))
                y += 40
        else:
            info = font.render('No saved games.', True, (0,0,0))
            surface.blit(info, (60, y))

    def draw_default(self, surface):
        pass

    def cleanup(self):
        self.clear_buttons()

    def handle_event(self, event):
        """Handle UI events such as button clicks and key presses."""
        for button in self.buttons:
            button.handle_event(event)

        if self.current_screen == 'settings':
            y1 = 210
            y2 = 360
            x_left = 100
            x_center = DEFAULTS.VIRTUAL_WIDTH // 2 - 80
            x_right = DEFAULTS.VIRTUAL_WIDTH - 250

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if hasattr(DEFAULTS, "SCALE"):
                    mouse_x = int(mouse_x * DEFAULTS.SCALE)
                    mouse_y = int(mouse_y * DEFAULTS.SCALE)
                # Obsługa change_buttonów
                for btn in self.get_change_buttons():
                    if btn["rect"].collidepoint((mouse_x, mouse_y)):
                        self.awaiting_key = btn["key"]
                # Slider
                if self.slider_rect.collidepoint((mouse_x, mouse_y)):
                    rel_x = mouse_x - self.slider_rect.x
                    rel_x = max(0, min(rel_x, self.slider_rect.width))
                    self.music_volume = rel_x / self.slider_rect.width
                    pygame.mixer.music.set_volume(self.music_volume)

        if hasattr(self, "awaiting_key") and event.type == pygame.KEYDOWN:
            player, action = self.awaiting_key
            controls = storage_service.get_controls()
            controls[player][action] = event.key
            storage_service.save_controls(controls)
            del self.awaiting_key

    def change_controls_p1(self):
        self.awaiting_key = ("player1", "left")  # potem "right", "hit"
        print("Naciśnij nowy klawisz dla: Lewo (P1)")

    def change_controls_p2(self):
        self.awaiting_key = ("player2", "left")  # potem "right", "hit"
        print("Naciśnij nowy klawisz dla: Lewo (P2)")

    def show_history(self):
        """Display the game history screen with a list of previous games."""
        games = storage_service.get_all_history_records()
        self.clear_buttons()
        self.buttons.append(Button(400, 50, self.assets['return'], self.show_settings))
        self.current_screen = 'history'
        self.history_games = games  # zapisz do późniejszego rysowania

    def get_change_buttons(self):
        # Zwraca listę słowników z pozycjami i identyfikatorem akcji
        y1 = 210
        y2 = 360
        x_left = 100
        x_center = DEFAULTS.VIRTUAL_WIDTH // 2 - 80
        x_right = DEFAULTS.VIRTUAL_WIDTH - 250
        btn_w = self.assets['change_button'].get_width()
        btn_h = self.assets['change_button'].get_height()
        return [
            {"rect": pygame.Rect(x_left, y1, btn_w, btn_h), "key": ("player1", "left")},
            {"rect": pygame.Rect(x_center, y1, btn_w, btn_h), "key": ("player1", "hit")},
            {"rect": pygame.Rect(x_right, y1, btn_w, btn_h), "key": ("player1", "right")},
            {"rect": pygame.Rect(x_left, y2, btn_w, btn_h), "key": ("player2", "left")},
            {"rect": pygame.Rect(x_center, y2, btn_w, btn_h), "key": ("player2", "hit")},
            {"rect": pygame.Rect(x_right, y2, btn_w, btn_h), "key": ("player2", "right")},
        ]
