import pygame
import constants as c


class Sword(pygame.sprite.Sprite):
    """ Sword's Hitbox """
    def __init__(self, x, y, flip):
        super().__init__()
        self.rect = pygame.Rect(x, y, 29, 39)
        self.flip = flip

        self.collided = False
        self.hitbox = pygame.Rect(x + 39, y + 33, 26, 18)

    def update(self, group,  screen, x, y, flip, attack_frame):
        # sword comes out frame 2
        if not self.collided and attack_frame >= 3:
            self.check_collision(group)

        self.draw(screen, x, y, flip)

    def check_collision(self, enemy_group):
        for enemy in enemy_group:
            if pygame.Rect.colliderect(self.hitbox, enemy.hitbox):
                # to play hurt animation
                enemy.action_index = c.HURT_IDX

                # ensure only counts 1 collision per attack
                if enemy.alive and not self.collided:
                    self.collided = True
                    enemy.health -= 1
            else:
                enemy.action_index = c.IDLE_IDX

    def draw(self, surf, x, y, flip):
        # adjust hitbox
        if flip:
            self.hitbox = pygame.Rect(x - 2, y + 33, 24, 18)
        else:
            self.hitbox = pygame.Rect(x + 39, y + 33, 26, 18)
        pygame.draw.rect(surf, 'red', self.hitbox, 1)
