import pygame
from src import constants as c
from src import utility


class Effect(pygame.sprite.Sprite):
    path = 'assets/player/dust_effect'

    def __init__(self, type, pos):
        super().__init__()
        if type == c.JUMP_IDX:
            self.animation_list = utility.load_images(f'{self.path}/jump/*.png')
        if type == c.LAND_IDX:
            self.animation_list = utility.load_images(f'{self.path}/land/*.png')

        self.current_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift

    def animate(self):
        # increment frame index based on action's cooldown
        self.image = self.animation_list[self.frame_index]
        if (pygame.time.get_ticks() - self.current_time) > c.DUST_ANI:
            self.current_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list):
            self.kill()
