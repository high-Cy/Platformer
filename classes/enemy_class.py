import pygame
import os
from random import randint
import constants as c
import utility


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_list = []
        self.action_index = c.IDLE_IDX
        self.current_time = pygame.time.get_ticks()

        self.frame_index = 0
        self.flip = False
        self.direction = 1

        self.move_counter = 0
        self.idle_counter = 0
        self.move_right = False
        self.move_left = False
        self.speed = c.ENEMY_SPEED

        self.alive = True

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def draw(self, surf):
        img = pygame.transform.flip(self.image, self.flip, False)
        surf.blit(img, self.rect)



class Slime01(Enemy):
    def __init__(self, x, y):
        super().__init__()
        self.load_images()

        self.cooldowns = [c.IDLE_ANI, c.RUN_ANI_2, c.DEAD_ANI, c.HURT_ANI]

        self.image = self.animation_list[0][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        self.health = 2
        self.hitbox = (self.rect.x + 2, self.rect.y + 9, 30, 25)
        self.vision = pygame.Rect(0, 0, 150, 25)

    def load_images(self):
        frame_type = ['idle', 'move', 'die', 'hurt']
        for animation in frame_type:
            tmp_list = []
            num_frames = len(os.listdir(f'slime01/slime01-{animation}'))
            for i in range(num_frames):
                fn = f'slime01/slime01-{animation}/slime-{animation}-{i}.png'

                img = pygame.image.load(fn).convert_alpha()
                img = pygame.transform.scale(img, (32, 32))
                tmp_list.append(img)

            self.animation_list.append(tmp_list)

    def update(self, screen):
        if self.alive:
            self.ai()
            self.check_alive()

        else:
            utility.update_action(self, c.DEAD_IDX)
            # kill after finish death animation and timer
            if self.frame_index == len(
                    self.animation_list[self.action_index]) - 1 and (
                    pygame.time.get_ticks() - self.current_time) > c.KILL_TIMER:
                self.kill()

        self.animate()
        self.draw(screen)

    def ai(self):
        if self.action_index == c.RUN_IDX:
            if randint(1, 300) == 1:
                utility.update_action(self, c.IDLE_IDX)
            else:
                if self.direction == 1:
                    self.move_right = True
                else:
                    self.move_right = False

                self.move_left = not self.move_right
                if self.action_index != c.HURT_IDX:
                    self.move()
                    self.move_counter += 1

                if self.move_counter > c.MOVE_COUNTER:
                    self.direction *= -1
                    self.move_counter *= -1

        elif self.action_index == c.IDLE_IDX:
            self.idle_counter += 1
            if self.idle_counter >= c.IDLE_COUNTER:
                self.idle_counter = 0
                utility.update_action(self, c.RUN_IDX)

    def move(self):
        utility.update_action(self, c.RUN_IDX)

        # reset movement variables
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if self.move_left:
            dx = -self.speed
            self.flip = False
            self.direction = -1
        if self.move_right:
            dx = self.speed
            self.flip = True
            self.direction = 1

        # check collision with floor
        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom


        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def animate(self):
        # increment frame index based on action's cooldown
        self.image = self.animation_list[self.action_index][self.frame_index]
        if (pygame.time.get_ticks() - self.current_time) > \
                self.cooldowns[self.action_index]:
            self.current_time = pygame.time.get_ticks()
            self.frame_index += 1

        # reset frame index
        if self.frame_index >= len(self.animation_list[self.action_index]):
            # only play dead / hurt animation once
            if self.action_index == c.DEAD_IDX:
                self.frame_index = len(
                    self.animation_list[self.action_index]) - 1
            elif self.action_index == c.HURT_IDX:
                utility.update_action(self, c.IDLE_IDX)
                self.frame_index = 0
            else:
                self.frame_index = 0

    def draw(self, surf):
        img = pygame.transform.flip(self.image, self.flip, False)
        surf.blit(img, self.rect)

        # adjust hitbox and vision
        self.hitbox = (self.rect.x + 2, self.rect.y + 9, 30, 25)
        self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery+5)

        pygame.draw.rect(surf, 'red', self.hitbox, 1)
        pygame.draw.rect(surf, 'blue', self.vision, 2)
