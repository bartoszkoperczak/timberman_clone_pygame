import pygame

from src.Drawable import Drawable
from src.button import Button

class UIManager(Drawable): # dodalem ze musi byc drawable
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

    # dodalem virtual surface wiec wszystkie obiekty sa rozmieszczone na powierzchni 1000x563, a dopiero potem skalowane do rozmiaru okna

    def create_main_menu(self):
        print("Creating main menu")
        self.clear_buttons()
        self.buttons = [
            Button(400, 50, self.assets['singleplayer'], self.game_window.start_singleplayer),
            Button(400, 150, self.assets['multiplayer'], self.show_multiplayer_menu),
            Button(400, 300, self.assets['settings'], self.show_settings),
            Button(400, 450, self.assets['quit'], self.game_window.quit_game)
        ]
        self.current_screen = 'main'

    def show_multiplayer_menu(self):
        print("Creating multiplayer menu")
        self.clear_buttons()
        self.buttons = [
            Button(400, 50, self.assets['1vs1'], self.game_window.start_1vs1),
            Button(400, 200, self.assets['1vsbot'], self.game_window.start_1vsbot),
            Button(400, 350, self.assets['return'], self.create_main_menu),
        ]
        self.current_screen = 'multiplayer'

    def show_settings(self):
        print("Creating settings menu")
        self.clear_buttons()
        # Placeholder - add volume control or other settings later
        self.buttons = [
            Button(400, 133, self.assets['return'], self.create_main_menu),
        ]
        self.current_screen = 'settings'

    # gdzies byl memory leak i buttony zostawaly w pamieci co powodowalo brak unregisterowania eventow
    def clear_buttons(self):
        for button in self.buttons:
            button.unregister()
        self.buttons.clear()

    def quit_game(self):
        pygame.quit()
        exit()

    def draw(self, surface):
        surface.fill((173, 216, 230))
        for button in self.buttons:
            button.draw(surface)

