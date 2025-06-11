import pygame
from src.event_manager import event_manager
from src.ui_manager import UIManager
from src.game.Game import Game, GameMode
from src.view_manager import view_manager
from src import DEFAULTS

class GameWindow:
    def __init__(self):
        """Initialize the game window, UI, music, and main view."""
        pygame.init()
        pygame.display.set_caption("TimbermanClone")
        self.running = True
        self.clock = pygame.time.Clock()
        self.view_manager = view_manager
        self.ui_manager = UIManager(self, self.view_manager)
        self.view_manager.change_view(self.ui_manager)

        # --- MUZYKA W TLE ---
        pygame.mixer.init()
        pygame.mixer.music.load("assets/background-music.mp3")
        pygame.mixer.music.set_volume(0.3)  # domyślna głośność (0.0 - 1.0)
        pygame.mixer.music.play(-1)  # zapętl muzykę

    def run(self):
        """Main application loop: handle events and update the view."""
        while self.running:
            events = pygame.event.get()  # Zbierz wszystkie eventy do zmiennej
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                view_manager.current_view.handle_event(event)

            for listener in event_manager.loop_listeners:
                listener()

            self.view_manager.draw()
            self.clock.tick(DEFAULTS.FPS)

        pygame.quit()
    
    def start_singleplayer(self):
        print("Uruchamiam tryb singleplayer")
        Game(GameMode.SINGLE_PLAYER, self)

    def start_1vs1(self):
        print("Uruchamiam tryb 1vs1")
        Game(GameMode.MULTI_PLAYER, self)

    def start_1vsbot(self):
        print("Uruchamiam tryb 1vsbot")
        Game(GameMode.VS_BOT, self)

    def quit_game(self):  # Jeśli jeszcze tego nie masz
        pygame.quit()
        exit()

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

        if self.current_screen == 'settings':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print("MOUSEBUTTONDOWN", event.pos)
                if self.slider_rect.collidepoint(event.pos):
                    print("Slider clicked!")
                    self.slider_dragging = True
                    rel_x = event.pos[0] - self.slider_rect.x
                    rel_x = max(0, min(rel_x, self.slider_rect.width))
                    self.music_volume = rel_x / self.slider_rect.width
                    pygame.mixer.music.set_volume(self.music_volume)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                print("MOUSEBUTTONUP")
                self.slider_dragging = False
            elif event.type == pygame.MOUSEMOTION and self.slider_dragging:
                print("MOUSEMOTION", event.pos)
                rel_x = event.pos[0] - self.slider_rect.x
                rel_x = max(0, min(rel_x, self.slider_rect.width))
                self.music_volume = rel_x / self.slider_rect.width
                pygame.mixer.music.set_volume(self.music_volume)

game_window = GameWindow()