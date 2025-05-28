import pygame

from src.event_manager import event_manager
from src.ui_manager import UIManager


class GameWindow:
    def __init__(self):
        pygame.init()
        self.width = 1500
        self.height = 844
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("TimbermanClone")
        self.running = True
        self.clock = pygame.time.Clock()
        self.ui_manager = UIManager(self)

    def run(self):
        while self.running:
            keys_pressed = pygame.key.get_pressed()
            event_manager.parse_keys(keys_pressed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.ui_manager.handle_event(event)

            self.ui_manager.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
    
    def start_singleplayer(self):
        print("Uruchamiam tryb singleplayer")
        # Tutaj dodasz później logikę gry

    def start_1vs1(self):
        print("Uruchamiam tryb 1vs1")
        # Tutaj dodasz później logikę gry

    def start_1vsbot(self):
        print("Uruchamiam tryb 1vsbot")
        # Tutaj dodasz później logikę gry

    def quit_game(self):  # Jeśli jeszcze tego nie masz
        pygame.quit()
        exit()



game_window = GameWindow()