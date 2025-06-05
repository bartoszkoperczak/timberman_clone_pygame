import os
import pygame

class AssetsManager:
    def __init__(self, assets_dir='assets'):
        self.assets_dir = assets_dir
        self.images = {}
        self.loaded = False

    def _load_images(self):
        for root, dirs, files in os.walk(self.assets_dir):
            for filename in files:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    name = os.path.splitext(filename)[0]
                    path = os.path.join(root, filename)
                    self.images[name] = pygame.image.load(path).convert_alpha()

    def get(self, name):
        if not self.loaded:
            self._load_images()
            self.loaded = True

        return self.images.get(name)
    

assets = AssetsManager()