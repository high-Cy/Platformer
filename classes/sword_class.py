import pygame

class Sword(pygame.sprite.Sprite):
    """ Sword's Hitbox """
    def __init__(self, x, y, flip):
        super().__init__()
        self.rect = pygame.Rect(x, y, 29, 39)
        self.flip = flip

        self.hitbox = (x + 39, y + 33, 26, 18)

    def draw(self, surf, x, y, flip):
        # adjust hitbox
        if flip:
            self.hitbox = (x -2, y + 33, 24, 18)
        else:
            self.hitbox = (x + 39, y + 33, 26, 18)
        pygame.draw.rect(surf, 'red', self.hitbox, 1)
