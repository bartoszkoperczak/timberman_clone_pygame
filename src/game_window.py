import pygame
from src.event_manager import event_manager
from src.ui_manager import UIManager
from src.game.Game import Game, GameMode
from src.view_manager import ViewManager
from src import DEFAULTS

class GameWindow:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TimbermanClone")
        self.running = True
        self.clock = pygame.time.Clock()
        self.ui_manager = UIManager(self)
        self.view_manager = ViewManager(self.ui_manager)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                event_manager.handle_event(event)

            self.view_manager.draw()
            self.clock.tick(DEFAULTS.FPS)

        pygame.quit()
    
    def start_singleplayer(self):
        print("Uruchamiam tryb singleplayer")
        Game(GameMode.SINGLE_PLAYER)

    def start_1vs1(self):
        print("Uruchamiam tryb 1vs1")
        Game(GameMode.MULTI_PLAYER)

    def start_1vsbot(self):
        print("Uruchamiam tryb 1vsbot")
        Game(GameMode.VS_BOT)

    def quit_game(self):  # Jeśli jeszcze tego nie masz
        pygame.quit()
        exit()



game_window = GameWindow()