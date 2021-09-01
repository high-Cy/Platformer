import pygame
from src import utility as u
from src import constants as c


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, screen, shift):
        self.draw(screen)
        self.rect.x += shift

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class StaticTile(Tile):
    def __init__(self, size, pos, surface):
        super().__init__(size, pos)
        self.image = surface


class AnimatedTile(Tile):
    def __init__(self, size, pos, path):
        super().__init__(size, pos)
        self.frames = u.load_images(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.current_time = pygame.time.get_ticks()

    def update(self, screen, shift):
        self.animate()
        self.draw(screen)
        self.rect.x += shift

    def animate(self):
        self.image = self.frames[self.frame_index]
        if (pygame.time.get_ticks() - self.current_time) > \
                c.TILE_ANI:
            self.current_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.frames):
            self.frame_index = 0

class Palm(AnimatedTile):
    def __init__(self, size, pos, path, offset):
        super().__init__(size, pos, path)
        offset_y = pos[1] - offset
        self.rect.topleft = (pos[0], offset_y)



