import pygame
from random import randint
from src.constants import *
from src.utility import *

class Enemy(pygame.sprite.Sprite):
    path = 'assets/enemy'

    def __init__(self, x, y):
        super().__init__()

        self.killed_sound = pygame.mixer.Sound('assets/sound/effects/enemy_die.wav')
        self.killed_sound.set_volume(0.7)

        self.animation_dict = {}
        self.action = IDLE_IDX
        self.current_time = pygame.time.get_ticks()

        self.frame_index = 0
        self.flip = True
        self.direction = 1

        self.move_counter = 0
        self.idle_counter = 0
        self.move_right = False
        self.move_left = False
        self.speed = ENEMY_SPEED

        self.alive = True

    def load_images(self, frame_types, enemy_name, scale):
        img_path = f'{self.path}/{enemy_name}'
        for animation in frame_types:
            self.animation_dict[animation] = load_images(
                f'{img_path}/{animation}/*.png', scale=scale)

    def check_alive(self):
        if self.health <= 0:
            self.killed_sound.play()
            self.health = 0
            self.alive = False

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, self.rect)


class WeakEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 1

    def update(self, screen, shift, constraints):
        if self.alive:
            self.ai(constraints)
            self.check_alive()

        else:
            update_action(self, DEAD_IDX)
            # kill after finish death animation and timer
            if self.frame_index == len(
                    self.animation_dict[self.action]) - 1 and (
                    pygame.time.get_ticks() - self.current_time) > KILL_TIMER:
                self.kill()

        self.rect.x += shift
        self.animate()
        self.draw(screen)

    def ai(self, constraints):
        if self.action == RUN_IDX:
            if randint(1, 300) == 1:
                update_action(self, IDLE_IDX)
            else:
                self.move()

                # turn around
                if pygame.sprite.spritecollideany(self, constraints):
                    self.direction *= -1
                    self.flip = not self.flip

            # if pygame.Rect.colliderect(self.vision, player_hitbox):
            #     self.speed = ENEMY_SPEED_2
            # else:
            #     self.speed = ENEMY_SPEED

        elif self.action == IDLE_IDX:
            self.idle_counter += 1
            if self.idle_counter >= IDLE_COUNTER:
                self.idle_counter = 0
                update_action(self, RUN_IDX)

    def move(self):
        update_action(self, RUN_IDX)

        # update rectangle position
        self.rect.x += (self.direction * self.speed)

    def animate(self):
        # increment frame index based on action's cooldown
        self.image = self.animation_dict[self.action][self.frame_index]
        if (pygame.time.get_ticks() - self.current_time) > \
                self.cooldowns[self.action]:
            if self.alive:
                self.current_time = pygame.time.get_ticks()
            self.frame_index += 1

        # reset frame index
        if self.frame_index >= len(self.animation_dict[self.action]):
            # only play dead / hurt animation once
            if self.action == DEAD_IDX:
                self.frame_index = len(
                    self.animation_dict[self.action]) - 1
            elif self.action == HIT_IDX:
                update_action(self, RUN_IDX)
                self.frame_index = 0
            else:
                self.frame_index = 0


class Slime(WeakEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        frame_type = [IDLE_IDX, RUN_IDX, DEAD_IDX, HIT_IDX]
        self.load_images(frame_types=frame_type, enemy_name='slime', scale=1.2)

        self.cooldowns = {
            IDLE_IDX: IDLE_ANI, RUN_IDX: RUN_ANI,
            DEAD_IDX: DEAD_ANI, HIT_IDX: HURT_ANI
        }
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect = self.image.get_rect(midtop=(x, y))
        self.rect.y += 35

        self.hitbox = pygame.Rect(0, 0, 30, 24)
        self.vision = pygame.Rect(0, 0, 150, 25)

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, self.rect)

        # adjust hitbox and vision
        self.hitbox.center = (self.rect.centerx + 2, self.rect.centery + 7)
        self.vision.center = (
            self.rect.centerx + 75 * self.direction, self.rect.centery + 5)

        pygame.draw.rect(screen, 'red', self.hitbox, 1)
        pygame.draw.rect(screen, 'blue', self.vision, 2)


class Worm(WeakEnemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        frame_type = [IDLE_IDX, RUN_IDX, DEAD_IDX]
        self.load_images(frame_types=frame_type, enemy_name='worm', scale=1.2)

        self.cooldowns = {
            IDLE_IDX: IDLE_ANI, RUN_IDX: RUN_ANI, DEAD_IDX: DEAD_ANI
        }
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect = self.image.get_rect(midtop=(x, y))
        self.rect.y += 30

        self.hitbox = pygame.Rect(0, 0, 40, 30)
        self.vision = pygame.Rect(0, 0, 150, 30)

    # def update(self, screen, shift, constraints):
    #     self.rect.x += shift
    #     self.draw(screen)

    def draw(self, surf):
        img = pygame.transform.flip(self.image, self.flip, False)
        surf.blit(img, self.rect)

        # adjust hitbox and vision
        self.hitbox.center = (self.rect.centerx, self.rect.centery + 3)
        self.vision.center = (
            self.rect.centerx + 75 * self.direction, self.rect.centery + 3)

        pygame.draw.rect(surf, 'red', self.hitbox, 1)
        pygame.draw.rect(surf, 'blue', self.vision, 2)
