import pygame
from src import constants as c, utility


class Sword(pygame.sprite.Sprite):
    """ Sword's Hitbox """

    def __init__(self, x, y, flip):
        super().__init__()
        self.rect = pygame.Rect(x, y, 29, 39)
        self.flip = flip

        self.collided = False
        self.hitbox = pygame.Rect(x + 39, y + 33, 26, 18)

    def update(self, enemies, screen, x, y, flip, attack_frame):
        self.check_collision(enemies, attack_frame)
        self.draw(screen, x, y, flip)

    def check_collision(self, enemy_group, attack_frame):
        # sword comes out frame 2
        if not self.collided and attack_frame >= 2:
            for enemy in enemy_group:
                if pygame.Rect.colliderect(self.hitbox,
                                           enemy.hitbox) and enemy.alive:
                    # to play hurt animation
                    if enemy.health > 1:
                        utility.update_action(enemy, c.HIT_IDX)

                    # ensure only counts 1 collision per attack
                    if not self.collided:
                        self.collided = True
                        enemy.health -= 1

    def draw(self, surf, x, y, flip):
        # adjust hitbox
        if flip:
            self.hitbox = pygame.Rect(x - 15, y + 20, 24,20)
        else:
            self.hitbox = pygame.Rect(x + 27, y + 20, 26, 20)

        pygame.draw.rect(surf, 'red', self.hitbox, 1)
