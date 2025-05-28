import pygame

from src.event_manager import event_manager


class GameWindow:
    def __init__(self):
        pygame.init()
        self.width = 1500
        self.height = 844
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("TimbermanClone")
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            keys_pressed = pygame.key.get_pressed()
            event_manager.parse_keys(keys_pressed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()



game_window = GameWindow()