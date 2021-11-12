import pygame, sys
from src.constants import *
from src.levels import Level
from src.overworld import Overworld
from src.ui import UI


class Game:
    def __init__(self):
        self.max_level = 0

        # overworld
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.level = None
        self.is_overworld = True

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld)
        self.is_overworld = False

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen,
                                   self.create_level)
        self.is_overworld = True

    def run(self):
        if self.is_overworld:
            self.overworld.run()
        else:
            self.level.run()


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    game.run()

    pygame.display.update()
    clock.tick(60)
