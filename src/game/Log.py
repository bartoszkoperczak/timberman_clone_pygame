import pygame
import random
import src.DEFAULTS as DEFAULTS
from src.assets_manager import assets
from src.interfaces.Drawable import Drawable



class Log(Drawable):
    def __init__(self, index, branch_state=None, bottommost_position=None):
        self.index = index
        is_golden, is_branch_golden = random.choices([False, True], weights=[97, 3], k=2)
        self.is_golden = is_golden
        self.is_branch_golden = is_branch_golden
        self.position = (bottommost_position[0], bottommost_position[1] - DEFAULTS.TREE_SIZE[1] * index)
        self.img = pygame.transform.scale(assets.get('golden_tree' if is_golden else 'tree'), DEFAULTS.TREE_SIZE)
        self.branch_img = pygame.transform.scale(assets.get('golden_branch' if is_branch_golden else 'branch'), DEFAULTS.TREE_SIZE)
        self.bottommost_position = bottommost_position
        self.branch_state = branch_state  # 0: no branch, -1: left branch, 1: right branch

        if self.branch_state is None:
            self.branch_state = random.choice([-1, 0, 1])

        if self.branch_state == -1:
            self.branch_img = pygame.transform.flip(self.branch_img, True, False)

        if self.branch_state != 0:
            self.branch_position = (self.position[0] + DEFAULTS.TREE_SIZE[0] * self.branch_state, self.position[1])

        # Animacja spadania
        self.falling = False
        self.fall_position = None
        self.fall_rotation = 0
        self.fall_start_time = None
        self.fall_side = 1  # 1 = prawo, -1 = lewo
        self.fall_x_speed = 0
        self.fall_y_speed = 0
        self.fall_rotation_speed = 0
        self.fall_scale = 1.0
        self.fall_scale_speed = 0
        self.fall_alpha = 255
        self.fall_alpha_speed = 0

    def start_falling(self):
        self.falling = True
        self.fall_position = list(self.position)
        self.fall_start_time = pygame.time.get_ticks()
        self.fall_rotation = 0

        self.fall_side = random.choice([-1, 1])
        self.fall_x_speed = random.uniform(150, 200) * self.fall_side      # px/s w bok
        self.fall_y_speed = random.uniform(200, 300)                      # px/s w dół
        self.fall_rotation_speed = random.uniform(90, 180) * self.fall_side # deg/s
        self.fall_scale = 1.0
        self.fall_scale_final = random.uniform(0.3, 0.7)                  # końcowa wielkość
        self.fall_scale_speed = (self.fall_scale_final - 1.0) / 0.8       # przez ok. 0.8s zmiana skali
        self.fall_alpha = 255
        self.fall_alpha_speed = -128                                      # znika w ok. 0.8s

    def animate_fall(self):
        if not self.falling:
            return False

        elapsed = (pygame.time.get_ticks() - self.fall_start_time) / 1000.0  # sekundy

        self.fall_position[0] = self.position[0] + self.fall_x_speed * elapsed
        self.fall_position[1] = self.position[1] + self.fall_y_speed * elapsed

        self.fall_rotation = self.fall_rotation_speed * elapsed

        new_scale = 1.0 + self.fall_scale_speed * elapsed
        self.fall_scale = max(self.fall_scale_final, new_scale)

        new_alpha = 255 + self.fall_alpha_speed * elapsed
        self.fall_alpha = max(0, min(255, int(new_alpha)))

        if self.fall_position[1] > self.bottommost_position[1] + 3 * DEFAULTS.TREE_SIZE[1] or self.fall_alpha <= 0:
            self.falling = False
            return True
        return False

    def draw_falling(self, screen):
        size = (
            int(DEFAULTS.TREE_SIZE[0] * self.fall_scale),
            int(DEFAULTS.TREE_SIZE[1] * self.fall_scale)
        )
        scaled_img = pygame.transform.smoothscale(self.img, size)
        rotated_img = pygame.transform.rotate(scaled_img, self.fall_rotation)
        rotated_img.set_alpha(self.fall_alpha)

        rect = rotated_img.get_rect(center=(
            self.fall_position[0] + DEFAULTS.TREE_SIZE[0] // 2,
            self.fall_position[1] + DEFAULTS.TREE_SIZE[1] // 2
        ))
        screen.blit(rotated_img, rect.topleft)

        if self.falling:
            if self.animate_fall():
                self.falling = False

    def update_index(self, index):
        self.index = index
        self.update_position()

    def update_position(self):
        self.position = (
            self.bottommost_position[0],
            self.bottommost_position[1] - DEFAULTS.TREE_SIZE[1] * (DEFAULTS.LOGS_PER_TREE - self.index - 1)
        )

        if self.branch_state != 0:
            self.branch_position = (self.position[0] + DEFAULTS.TREE_SIZE[0] * self.branch_state, self.position[1])

    def draw(self, screen):
        if self.branch_state != 0:
            screen.blit(self.branch_img, self.branch_position)
        screen.blit(self.img, self.position)