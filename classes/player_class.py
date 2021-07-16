import pygame
import os
import constants as c


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.alive = True

        # frames
        self.animation_list = []
        self.load_images()

        # animations
        self.cooldowns = [c.IDLE_COOL, c.RUN_COOL, c.DEAD_COOL, c.HURT_COOL,
                          c.ATTACK_COOL, c.JUMP_COOL]
        self.current_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action_index = c.IDLE_IDX
        self.image = self.animation_list[self.action_index][self.frame_index]
        self.rect = self.image.get_rect(center=(100, 400))
        self.flip = False
        self.direction = 1

        # movement
        self.move_right = False
        self.move_left = False
        self.in_air = False
        self.jump = False
        self.vel_y = 0
        self.speed = c.WALK_SPEED
        self.jump_vel = c.JUMP_VEL
        self.gravity = c.GRAVITY

    def load_images(self):
        # add frames to animation list
        frame_list = ['idle', 'run', 'dead', 'hurt', 'attack']
        for animation in frame_list:
            tmp_list = []
            num_frames = len(os.listdir(f'player_frames/{animation}'))
            for i in range(1, num_frames):
                fn = f'player_frames/{animation}/{animation}-{i}.png'
                img = pygame.transform.scale2x(pygame.image.load(fn).convert())
                tmp_list.append(img)

            self.animation_list.append(tmp_list)

        # jumping only has one frame
        jmp = f'player_frames/jump.png'
        img = pygame.transform.scale2x(pygame.image.load(jmp).convert())
        self.animation_list.append([img])

    def update_player(self, screen):
        # update action
        if self.in_air:
            self.update_action(c.JUMP_IDX)
        elif self.move_left or self.move_right:
            self.update_action(c.RUN_IDX)

        else:
            self.update_action(c.IDLE_IDX)


        self.move()
        self.draw(screen)
        self.animate()

    def update_action(self, new_action_idx):
        if new_action_idx != self.action_index:
            self.action_index = new_action_idx
            self.frame_index = 0
            self.current_time = pygame.time.get_ticks()

    def action(self):
        # gravity
        self.vel_y += self.gravity
        if self.rect.bottom + self.vel_y > 400:
            self.jump = False
            self.can_jump = True
            self.vel_y = 400 - self.rect.bottom
        # else:
        self.rect.y += self.gravity

        if self.action_index == c.RUN_IDX:
            self.running()
        elif self.action_index == c.JUMP_IDX:
            self.jumping()

    def move(self):
        # reset movement variables
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if self.move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if self.move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump and not self.in_air:
            self.vel_y += self.jump_vel
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += self.gravity
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom
            self.in_air = False
            self.jump = False

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def running(self):
        dx = 0
        if self.move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if self.move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        self.rect.x += dx

    def jumping(self):
        dy = 0
        if self.jump:
            dy += self.jump_vel

            self.can_jump = False

        self.rect.y += self.vel_y

    def animate(self):
        self.image = self.animation_list[self.action_index][self.frame_index]
        if (pygame.time.get_ticks() - self.current_time) > \
                self.cooldowns[self.action_index]:
            self.current_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action_index]):
            self.frame_index = 0

    def draw(self, surf):
        img = pygame.transform.flip(self.image, self.flip, False)
        surf.blit(img, self.rect)
