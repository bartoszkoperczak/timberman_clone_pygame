import pygame
from src.button import Button

class UIManager:
    def __init__(self, game_window):
        self.game_window = game_window
        self.current_screen = 'main'
        self.buttons = []
        self.assets = self.load_assets()
        self.create_main_menu()

    def load_assets(self):
        return {
            'singleplayer': pygame.image.load('assets/ui/singleplayer_button.png'),
            'multiplayer': pygame.image.load('assets/ui/multiplayer_button.png'),
            'settings': pygame.image.load('assets/ui/settings_button.png'),
            'quit': pygame.image.load('assets/ui/quit_button.png'),
            'return': pygame.image.load('assets/ui/return_button.png'),
            '1vs1': pygame.image.load('assets/ui/1vs1_button.png'),
            '1vsbot': pygame.image.load('assets/ui/1vsbot_button.png'),
        }

    def create_main_menu(self):
        self.buttons = [
            Button(600, 200, self.assets['singleplayer'], self.game_window.start_singleplayer),
            Button(600, 280, self.assets['multiplayer'], self.show_multiplayer_menu),
            Button(600, 360, self.assets['settings'], self.show_settings),
            Button(600, 440, self.assets['quit'], self.game_window.quit_game)
        ]
        self.current_screen = 'main'

    def show_multiplayer_menu(self):
        self.buttons = [
            Button(600, 200, self.assets['1vs1'], self.game_window.start_1vs1),
            Button(600, 280, self.assets['1vsbot'], self.game_window.start_1vsbot),
            Button(600, 360, self.assets['return'], self.create_main_menu),
        ]
        self.current_screen = 'multiplayer'

    def show_settings(self):
        # Placeholder - add volume control or other settings later
        self.buttons = [
            Button(600, 200, self.assets['return'], self.create_main_menu),
        ]
        self.current_screen = 'settings'

    def quit_game(self):
        pygame.quit()
        exit()

    def draw(self, surface):
        surface.fill((173, 216, 230))
        for button in self.buttons:
            button.draw(surface)

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)