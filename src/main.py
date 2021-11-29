import pygame, sys, json
from constants import *
from levels import Level
from overworld import Overworld


class Game:
    def __init__(self, saved_lvl):
        self.max_level = saved_lvl['max_level']

        self.level_bg = pygame.mixer.Sound('../assets/sound/level_music.wav')
        self.overworld_bg = pygame.mixer.Sound(
            '../assets/sound/overworld_music.wav')
        self.level_bg.set_volume(SOUND_VOLUME)
        self.overworld_bg.set_volume(SOUND_VOLUME)

        # overworld
        self.overworld = Overworld(saved_lvl['current_level'], self.max_level, screen,
                                   self.create_level, self.overworld_bg)
        self.level = None
        self.is_overworld = True
        self.overworld_bg.play(loops=-1)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld,
                           self.level_bg)
        saved_lvl['current_level'] = current_level
        self.is_overworld = False
        self.overworld_bg.stop()
        self.level_bg.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
            saved_lvl['max_level'] = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen,
                                   self.create_level, self.overworld_bg)
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
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(
    pygame.image.load('../assets/player/player_jump/jump-1.png'))
clock = pygame.time.Clock()

saved_lvl = {
    'current_level': 0,
    'max_level': 0
}
try:
    with open('saved_lvl.txt') as f:
        saved_lvl = json.load(f)
except:
    print('No file yet')

game = Game(saved_lvl)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('saved_lvl.txt', 'w') as f:
                json.dump(saved_lvl, f)

            pygame.quit()
            sys.exit()

    game.run()

    pygame.display.update()
    clock.tick(FPS)
