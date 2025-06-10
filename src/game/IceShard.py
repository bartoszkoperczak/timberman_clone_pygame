import pygame
import random
from src.assets_manager import assets
from src.interfaces.Obstacle import Obstacle

import src.DEFAULTS as DEFAULTS

class IceShard(Obstacle):
    def __init__(self, initial_position):
        super().__init__()
        self.side = random.choice([-1, 1])
        self.x = initial_position[0] + DEFAULTS.SPRITE_MOVEMENT_RANGE * (1 + self.side) / 2
        self.y = initial_position[1]
        self.speed = 3
        self.img = pygame.transform.scale(assets.get('ice_shard'), DEFAULTS.ICE_SHARD_SIZE)

    def collide_rect(self, other_rect):
        ice_shard_rect = pygame.Rect(self.x, self.y, DEFAULTS.ICE_SHARD_SIZE[0], DEFAULTS.ICE_SHARD_SIZE[1])
        return ice_shard_rect.colliderect(other_rect)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

