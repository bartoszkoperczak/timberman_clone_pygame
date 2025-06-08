import pygame
from src.interfaces.Drawable import Drawable
from src.assets_manager import assets
import src.DEFAULTS as DEFAULTS

class Character(Drawable):
    def __init__(self, initial_position, img_src='character_red'):
        self.hit_anim_frames = [
            pygame.transform.scale(assets.get(f'{img_src}_straight_pose'), DEFAULTS.SPRITE_SIZE),
            pygame.transform.scale(assets.get(f'{img_src}_swinging_pose'), DEFAULTS.SPRITE_SIZE),
            pygame.transform.scale(assets.get(f'{img_src}_chopping_pose'), DEFAULTS.SPRITE_SIZE),
        ]
        self.hit_anim_sequence = [0, 1, 2, 0]
        self.hit_anim_index = 0
        self.hit_animating = False
        self.img = self.hit_anim_frames[0]
        self.hit_anim_last_update = 0
        self.hit_anim_delay = DEFAULTS.ANIMATION_DURATION

        self.position = initial_position
        self.direction = -1
        self.img_alpha = 255

    def move(self, direction):
        if direction == self.direction:
            return

        self.hit_anim_frames = [pygame.transform.flip(frame, True, False) for frame in self.hit_anim_frames]
        self.img = self.hit_anim_frames[0]

        if direction == -1:
            self.position = (self.position[0] - DEFAULTS.SPRITE_MOVEMENT_RANGE, self.position[1])
            self.direction = -1
        elif direction == 1:
            self.direction = 1
            self.position = (self.position[0] + DEFAULTS.SPRITE_MOVEMENT_RANGE, self.position[1])

    def hit_animate(self):
        if not self.hit_animating:
            self.hit_animating = True
            self.hit_anim_index = 0
            self.hit_anim_last_update = pygame.time.get_ticks()
            self.img = self.hit_anim_frames[self.hit_anim_sequence[0]]

    def update(self):
        if self.hit_animating:
            now = pygame.time.get_ticks()
            if now - self.hit_anim_last_update >= self.hit_anim_delay:
                self.hit_anim_index += 1
                if self.hit_anim_index < len(self.hit_anim_sequence):
                    seq_idx = self.hit_anim_sequence[self.hit_anim_index]
                    self.img = self.hit_anim_frames[seq_idx]
                    self.hit_anim_last_update = now
                else:
                    self.hit_anim_index = 0
                    self.hit_animating = False
                    self.img = self.hit_anim_frames[self.hit_anim_sequence[0]]

    def set_transparency(self, alpha):
        self.img_alpha = alpha

    def hit(self):
        if not self.hit_animating:
            self.hit_animate()

    def draw(self, screen):
        self.img.set_alpha(self.img_alpha)
        screen.blit(self.img, self.position)
        self.update()

    def cleanup(self):
        pass
