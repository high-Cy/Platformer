import pygame
from constants import *
from utility import *


class Sword(pygame.sprite.Sprite):
    """ Sword's Hitbox """

    def __init__(self, x, y, flip):
        super().__init__()
        self.stab_sound = pygame.mixer.Sound('assets/sound/effects/stab.mp3')
        self.swing_sound = pygame.mixer.Sound('assets/sound/effects/swing.mp3')

        self.rect = pygame.Rect(x, y, 29, 39)
        self.flip = flip

        self.swung = False
        self.collided = False
        self.hitbox = pygame.Rect(x + 39, y + 33, 26, 18)

    def update(self, enemies, screen, x, y, flip, attack_frame, muted):
        self.check_collision(enemies, attack_frame, muted)
        self.draw(screen, x, y, flip)

    def check_collision(self, enemy_group, attack_frame, muted):
        # sword comes out frame 2
        if not self.collided and attack_frame >= 2:
            if not self.swung:
                if not muted:
                    self.swing_sound.play()
                self.swung = True
            for enemy in enemy_group:
                if pygame.Rect.colliderect(self.hitbox,
                                           enemy.hitbox) and enemy.alive:
                    # to play hurt animation
                    if enemy.health > 1:
                        update_action(enemy, HIT_IDX)
                        if not muted:
                            self.stab_sound.play()

                    # ensure only counts 1 collision per attack
                    if not self.collided:
                        self.collided = True
                        enemy.health -= 1

    def draw(self, surf, x, y, flip):
        # adjust hitbox
        if flip:
            self.hitbox = pygame.Rect(x - 20, y + 20, 28, 20)
        else:
            self.hitbox = pygame.Rect(x + 27, y + 20, 28, 20)

        # pygame.draw.rect(surf, 'red', self.hitbox, 1)
