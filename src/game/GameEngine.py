import pygame
import random
import src.DEFAULTS as DEFAULTS
from src.event_manager import event_manager
from src.game.Character import Character
from src.game.Tree import Tree
from src.game.IceShard import IceShard
from src.interfaces.Drawable import Drawable
from src.interfaces.EventSubscriber import EventSubscriber
from src.enums.SteeringMode import SteeringMode


class GameEngine(Drawable, EventSubscriber):
    def __init__(self, steering: SteeringMode, game_callback, rect):
        self.steering = steering
        self.game_callback = game_callback
        
        self.x_start, self.y_start = rect[0]
        self.x_end, self.y_end = rect[1]
        self.width = self.x_end - self.x_start
        self.height = self.y_end - self.y_start

        self.untouchable_turns = 0

        self.character = Character(self.pos(self.width // 2 - DEFAULTS.SPRITE_SIZE[0] - DEFAULTS.TREE_SIZE[0] // 2, self.height - DEFAULTS.SPRITE_SIZE[1]), img_src='character_red' if steering == SteeringMode.PLAYER_1 else 'character_green')

        self.tree = Tree(self.pos(self.width // 2 - DEFAULTS.TREE_SIZE[0] // 2 , self.height - DEFAULTS.TREE_SIZE[1]))

        if steering != SteeringMode.BOT:
            self.steering = DEFAULTS.PLAYER_1_STEERING if steering == SteeringMode.PLAYER_1 else DEFAULTS.PLAYER_2_STEERING
            event_manager.register_listener(pygame.KEYDOWN, self.register_listener)

        self.score = 0
        self.lost = False
        self.last_points = 0
        self.last_points_time = 0
        self.points_popups = []  # lista popupów punktów
        self.ice_shard = None

    def register_listener(self, e):
        # Blokada po przegranej
        if hasattr(self, 'lost') and self.lost:
            return
        if e.key == self.steering['left']:
            self.handle_lclick()
        elif e.key == self.steering['right']:
            self.handle_rclick()
        elif e.key == self.steering['hit']:
            self.handle_hit()

    def handle_rclick(self):
        self.character.move(1)
        self.check_collision()

    def handle_lclick(self):
        self.character.move(-1)
        self.check_collision()

    def handle_hit(self):
        if self.ice_shard is None and random.random() < DEFAULTS.ICE_SHARD_CHANCE:
            self.ice_shard = IceShard(self.pos(self.width // 2 - DEFAULTS.ICE_SHARD_SIZE[0] - DEFAULTS.TREE_SIZE[0] // 2, 0))

        self.character.hit()
        self.game_callback("score", None)
        is_golden, is_branch_golden = self.tree.drop()
        pts_amount = 10 if is_golden else 1

        if is_branch_golden:
            self.untouchable_turns = 15

        self.increment_score(pts_amount)

        if self.untouchable_turns > 0:
            self.untouchable_turns -= 1
            self.character.set_transparency(128)
        else:
            self.check_collision()
            self.character.set_transparency(255)

    def pos(self, x=0, y=0):
        return self.x_start + x, self.y_start + y - DEFAULTS.GAME_BOTTOM_OFFSET

    def draw(self, screen, *args):
        self.character.draw(screen)
        self.tree.draw(screen)
        self._draw_points_popup(screen)

        if self.ice_shard is not None:
            self.ice_shard.update()
            self.ice_shard.draw(screen)
            collided = self.check_ice_shard_collision()

            if self.ice_shard.y > self.height or collided:
                self.ice_shard = None

    def _draw_points_popup(self, screen):
        duration = 400  # ms
        base_size = 36
        for popup in self.points_popups[:]:
            elapsed = pygame.time.get_ticks() - popup['time']
            if elapsed < duration:
                scale = 1 + 0.3 * (elapsed / duration) + abs(popup['amount'] / 30) * 2
                font_size = int(base_size * scale)
                font = pygame.font.Font("assets/fonts/Pixelify_Sans/static/PixelifySans-Bold.ttf", font_size)

                color = (255, 215, 0) if popup['amount'] >= 0 else (255, 0, 0)
                sign = "+" if popup['amount'] >= 0 else ""
                points_text = font.render(f"{sign}{popup['amount']}", True, color)

                text_rect = points_text.get_rect(center=(popup['x'], popup['y']))
                screen.blit(points_text, text_rect)
            else:
                self.points_popups.remove(popup)

    def check_ice_shard_collision(self):
        if self.ice_shard is not None:
            # Pobierz prostokąt postaci
            char_rect = pygame.Rect(self.character.position, self.character.img.get_size())

            if self.ice_shard.collide_rect(char_rect) and self.untouchable_turns <= 0:
                self.increment_score(-30)
                return True
        return False

    def check_collision(self):
        if self.untouchable_turns > 0:
            return
        # Sprawdź czy character jest na tej samej stronie co branch w najniższym logu
        lowest_log = self.tree.stack[-1]
        if lowest_log.branch_state != 0 and self.character.direction == lowest_log.branch_state:
            self.game_callback("lose", None)

    def increment_score(self, amount=1):
        self.score += amount
        self.last_points = amount
        self.last_points_time = pygame.time.get_ticks()
        x = random.randint(-20, 20)
        y = random.randint(-20, 20)
        self.points_popups.append({
            'amount': amount,
            'time': pygame.time.get_ticks(),
            'x': self.character.position[0] + x,
            'y': self.character.position[1] - y
        })


    def unregister(self):
        if self.steering != SteeringMode.BOT:
            event_manager.unregister_listener(pygame.KEYDOWN, self.register_listener)

