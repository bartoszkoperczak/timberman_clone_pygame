import pygame
import random
import src.DEFAULTS as DEFAULTS
from src.assets_manager import assets
from src.interfaces.Drawable import Drawable
from src.game.Log import Log

    


class Tree(Drawable):
    def __init__(self, bottommost_position):
        self.bottommost_position = bottommost_position
        self.falling_logs = []
        self.stack = []

        for i in range(0, DEFAULTS.LOGS_PER_TREE):
            self.add_log(i)


        # kloda na samym dole ma najwyzszy indeks, a ta na samej gorze najnizszy
    def add_log(self, index):
        if len(self.stack) == 0:
            self.stack.append(Log(index, branch_state=0, bottommost_position=self.bottommost_position))
            return

        previous_log = self.stack[0] # -1 
        previous_branch_state = previous_log.branch_state
        branch_state_options = [-1, 0, 1]
        branch_state_options.remove(-previous_branch_state)
        branch_state = random.choice(branch_state_options)
        new_log = Log(index, branch_state=branch_state, bottommost_position=self.bottommost_position)

        self.stack.insert(0, new_log)

    def drop(self):
        falling_log = self.stack.pop()
        falling_log.start_falling()
        self.update_falling_logs(falling_log)
        self.add_log(0)

        for i, log in enumerate(self.stack):
            log.update_index(i)

    def update_falling_logs(self, new):
        for log in self.falling_logs:
            if not log.falling:
                self.falling_logs.remove(log)

        self.falling_logs.append(new)



    def draw(self, screen):
        for log in self.stack:
            log.draw(screen)


        for log in self.falling_logs:
            log.draw_falling(screen)
    