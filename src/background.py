import pygame
from random import choice, randint
from constants import *
from utility import *
from tiles import AnimatedTile, StaticTile

path = '../assets/terrain/decoration'


class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load(f'{path}/sky/sky_top.png')
        self.mid = pygame.image.load(f'{path}/sky/sky_middle.png')
        self.bot = pygame.image.load(f'{path}/sky/sky_bottom.png')
        self.horizon = horizon

        self.top = pygame.transform.scale(self.top, (SCREEN_WIDTH, TILE_SIZE))
        self.mid = pygame.transform.scale(self.mid, (SCREEN_WIDTH, TILE_SIZE))
        self.bot = pygame.transform.scale(self.bot, (SCREEN_WIDTH, TILE_SIZE))

    def draw(self, screen):
        for row in range(TILE_NUM_Y):
            y = row * TILE_SIZE
            if row < self.horizon:
                screen.blit(self.top, (0,y))
            elif row == self.horizon:
                screen.blit(self.mid, (0,y))
            else:
                screen.blit(self.bot, (0,y))


class Water:
    def __init__(self, top, level_width):
        water_start = -SCREEN_WIDTH
        water_width = 192
        num_tiles = int((level_width + SCREEN_WIDTH) / water_width) + 10
        self.water_sprites = pygame.sprite.Group()

        for tile in range(num_tiles):
            x = tile * water_width + water_start
            y = top
            sprite = AnimatedTile(TILE_SIZE, (x,y), f'{path}/water/*.png')
            self.water_sprites.add(sprite)

    def update(self, screen, shift):
        self.water_sprites.update(screen, shift)


class Clouds:
    def __init__(self, horizon, level_width, cloud_number):
        cloud_list = load_images(f'{path}/clouds/*.png')
        min_x = -SCREEN_WIDTH
        max_x = level_width + SCREEN_WIDTH
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(0, (x,y), cloud)
            self.cloud_sprites.add(sprite)

    def update(self, screen, shift):
        self.cloud_sprites.update(screen, shift)
