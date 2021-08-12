import pygame
from random import randint
import constants as c
import utility


class Enemy(pygame.sprite.Sprite):
    path = 'assets/enemy'

    def __init__(self):
        super().__init__()
        self.animation_dict = {}
        self.action = c.IDLE_IDX
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

    def load_images(self, frame_types, enemy_name):
        img_path = f'{self.path}/{enemy_name}'
        lst = ["%.2d" % i for i in range(1, len(img_path)+1)]
        i = 0
        for animation in frame_types:
            self.animation_dict[animation] = utility.load_images(
                f'{img_path}/{animation}/*.png')

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
        frame_type = [c.IDLE_IDX, c.RUN_IDX, c.DEAD_IDX, c.HIT_IDX]
        self.load_images(frame_types=frame_type, enemy_name='slime')

        self.cooldowns = {
            c.IDLE_IDX: c.IDLE_ANI, c.RUN_IDX: c.RUN_ANI,
            c.DEAD_IDX: c.DEAD_ANI, c.HIT_IDX: c.HURT_ANI
        }
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        self.health = 2
        self.hitbox = pygame.Rect(0, 0, 30, 24)
        self.vision = pygame.Rect(0, 0, 150, 25)


    def update(self, screen, player_hitbox):
        if self.alive:
            self.ai(player_hitbox)
            self.check_alive()

        else:
            utility.update_action(self, c.DEAD_IDX)
            # kill after finish death animation and timer
            if self.frame_index == len(
                    self.animation_dict[self.action]) - 1 and (
                    pygame.time.get_ticks() - self.current_time) > c.KILL_TIMER:
                self.kill()

        self.animate()
        self.draw(screen)

    def ai(self, player_hitbox):
        if self.action == c.RUN_IDX:
            if randint(1, 300) == 1:
                utility.update_action(self, c.IDLE_IDX)
            else:
                self.move_right = True if self.direction == 1 else False
                self.move_left = not self.move_right

                self.move()
                self.move_counter += 1

                if self.move_counter > c.MOVE_COUNTER:
                    self.direction *= -1
                    self.move_counter *= -1

            self.speed = c.ENEMY_SPEED_2 \
                if pygame.Rect.colliderect(self.vision, player_hitbox) \
                else c.ENEMY_SPEED

        elif self.action == c.IDLE_IDX:
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
        self.image = self.animation_dict[self.action][self.frame_index]
        if (pygame.time.get_ticks() - self.current_time) > \
                self.cooldowns[self.action]:
            self.current_time = pygame.time.get_ticks()
            self.frame_index += 1

        # reset frame index
        if self.frame_index >= len(self.animation_dict[self.action]):
            # only play dead / hurt animation once
            if self.action == c.DEAD_IDX:
                self.frame_index = len(
                    self.animation_dict[self.action]) - 1
            elif self.action == c.HIT_IDX:
                utility.update_action(self, c.RUN_IDX)
                self.frame_index = 0
            else:
                self.frame_index = 0

    def draw(self, surf):
        img = pygame.transform.flip(self.image, self.flip, False)
        surf.blit(img, self.rect)

        # adjust hitbox and vision
        self.hitbox.center = (self.rect.centerx + 2, self.rect.centery + 7)
        self.vision.center = (
            self.rect.centerx + 75 * self.direction, self.rect.centery + 5)

        pygame.draw.rect(surf, 'red', self.hitbox, 1)
        pygame.draw.rect(surf, 'blue', self.vision, 2)
