import pygame, sys
from src.constants import *
from src.levels import Level
from src.overworld import Overworld


class Game:
    def __init__(self):
        self.max_level = 0

        self.level_bg = pygame.mixer.Sound('assets/sound/level_music.wav')
        self.overworld_bg = pygame.mixer.Sound('assets/sound/overworld_music.wav')
        self.level_bg.set_volume(SOUND_VOLUME)
        self.overworld_bg.set_volume(SOUND_VOLUME)

        # overworld
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.level = None
        self.is_overworld = True
        self.overworld_bg.play(loops=-1)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.level_bg)
        self.is_overworld = False
        self.overworld_bg.stop()
        self.level_bg.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen,
                                   self.create_level)
        self.is_overworld = True
        self.overworld_bg.play(loops=-1)
        self.level_bg.stop()


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
