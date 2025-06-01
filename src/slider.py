import pygame

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val, bar_img):
        self.x = x
        self.y = y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.bar_img = bar_img
        self.bar_height = bar_img.get_height()
        self.handle_radius = 9
        self.dragging = False

    def draw(self, surface):
        surface.blit(self.bar_img, (self.x, self.y))
        percent = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.x + int(percent * self.width)
        handle_y = self.y + self.bar_height // 2
        pygame.draw.circle(surface, (60, 60, 60), (handle_x, handle_y), self.handle_radius)
        pygame.draw.circle(surface, (180, 180, 180), (handle_x, handle_y), self.handle_radius-4)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            percent = (self.value - self.min_val) / (self.max_val - self.min_val)
            handle_x = self.x + int(percent * self.width)
            handle_y = self.y + self.bar_height // 2
            if (mx - handle_x) ** 2 + (my - handle_y) ** 2 < self.handle_radius ** 2:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx = event.pos[0]
            rel_x = max(self.x, min(mx, self.x + self.width))
            percent = (rel_x - self.x) / self.width
            self.value = self.min_val + percent * (self.max_val - self.min_val)
            self.value = max(self.min_val, min(self.value, self.max_val))
