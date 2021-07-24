import pygame
import os
import constants as c


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_list = []

        self.frame_index = 0
        self.flip = False
        self.direction = 1

    def draw(self, surf):
        img = pygame.transform.flip(self.image, self.flip, False)
        surf.blit(img, self.rect)


class Slime01(Enemy):
    def __init__(self, x, y):
        super().__init__()
        self.load_images()

        self.cooldowns = [c.IDLE_ANI, c.RUN_ANI, c.DEAD_ANI, c.HURT_ANI]
        self.action_index = c.IDLE_IDX
        self.current_time = pygame.time.get_ticks()
        self.frame_index = 0

        self.image = self.animation_list[0][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        self.hitbox = (self.rect.x + 2, self.rect.y + 7, 30, 40)
        self.health = 2
        self.alive = True

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
        if not self.alive:
            self.action_index = c.DEAD_IDX
            # kill after finish death animation and timer
            if self.frame_index == len(
                    self.animation_list[self.action_index]) - 1 and (
                    pygame.time.get_ticks() - self.current_time) > c.KILL_TIMER:
                self.kill()

        self.check_alive()
        self.draw(screen)
        self.animate()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False

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
                self.action_index = c.IDLE_IDX
                self.frame_index = 0
            else:
                self.frame_index = 0

    def draw(self, surf):
        img = pygame.transform.flip(self.image, self.flip, False)
        surf.blit(img, self.rect)

        # adjust hitbox
        if self.flip:
            self.hitbox = (self.rect.x + 2, self.rect.y + 9, 30, 25)
        else:
            self.hitbox = (self.rect.x + 2, self.rect.y + 9, 30, 25)
        pygame.draw.rect(surf, 'red', self.hitbox, 1)
