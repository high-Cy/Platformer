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
        self.cooldowns = [c.IDLE_ANI, c.RUN_ANI, c.DEAD_ANI, c.HURT_ANI,
                          c.ATTACK_ANI, c.JUMP_ANI]
        self.current_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action_index = c.IDLE_IDX
        self.image = self.animation_list[self.action_index][self.frame_index]
        self.rect = self.image.get_rect(center=(100, 100))
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

        self.attack = False

        self.hitbox = pygame.Rect(self.rect.x + 11, self.rect.y + 15, 29, 39)

        self.health = 3
        self.max_health = self.health
        self.collided = False
        self.hurt_timer = None

    def load_images(self):
        # add frames to animation list
        frame_type = ['idle', 'run', 'dead', 'hurt', 'attack']
        for animation in frame_type:
            tmp_list = []
            num_frames = len(os.listdir(f'player/player_{animation}'))
            for i in range(1, num_frames):
                fn = f'player/player_{animation}/{animation}-{i}.png'
                img = pygame.transform.scale2x(pygame.image.load(fn).convert())
                tmp_list.append(img)

            self.animation_list.append(tmp_list)

        # jumping only has one frame
        jmp = f'player/player_jump.png'
        img = pygame.transform.scale2x(pygame.image.load(jmp).convert())
        self.animation_list.append([img])

    def update(self, screen, enemy_group):
        # update action when not hurt
        if self.action_index != c.HURT_IDX:
            if self.in_air:
                self.update_action(c.JUMP_IDX)
            elif self.move_left or self.move_right:
                self.update_action(c.RUN_IDX)
            elif self.attack:
                self.update_action(c.ATTACK_IDX)
            elif not self.alive:
                self.update_action(c.DEAD_IDX)

            else:
                self.update_action(c.IDLE_IDX)
            # can't move if hurt
            self.move()

        # Grants n amount of time of invincibility after hurt
        if self.hurt_timer and (
                pygame.time.get_ticks() - self.hurt_timer) >= c.HURT_TIMER:
            self.hurt_timer = None
            self.collided = False

        if self.alive:
            self.check_collision(enemy_group)
        self.animate()
        self.draw(screen)

    def update_action(self, new_action_idx):
        if new_action_idx != self.action_index:
            self.action_index = new_action_idx
            self.frame_index = 0
            self.current_time = pygame.time.get_ticks()

    def check_collision(self, enemy_group):
        for enemy in enemy_group:
            if pygame.Rect.colliderect(self.hitbox, enemy.hitbox):
                # ensure only counts 1 collision
                if enemy.alive and not self.collided:
                    self.update_action(c.HURT_IDX)
                    self.collided = True
                    self.health -= 1
                    self.hurt_timer = pygame.time.get_ticks()

                if self.health <= 0:
                    self.health = 0
                    self.alive = False

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

    def animate(self):
        # increment frame index based on action's cooldown
        self.image = self.animation_list[self.action_index][self.frame_index]
        if (pygame.time.get_ticks() - self.current_time) > \
                self.cooldowns[self.action_index]:
            self.current_time = pygame.time.get_ticks()
            self.frame_index += 1

        # reset frame index
        if self.frame_index >= len(self.animation_list[self.action_index]):
            self.frame_index = 0
            # only play player_attack animation once per key pressed
            if self.action_index == c.ATTACK_IDX:
                self.attack = False
            elif self.action_index == c.HURT_IDX:
                self.action_index = c.IDLE_IDX
            elif self.action_index == c.DEAD_IDX:
                self.frame_index = len(
                    self.animation_list[self.action_index]) - 1

    def draw(self, surf):
        img = pygame.transform.flip(self.image, self.flip, False)
        surf.blit(img, self.rect)

        # adjust hitbox
        if self.flip:
            self.hitbox = pygame.Rect(self.rect.x + 22, self.rect.y + 15, 29,
                                      39)
        else:
            self.hitbox = pygame.Rect(self.rect.x + 11, self.rect.y + 15, 29,
                                      39)
        pygame.draw.rect(surf, 'red', self.hitbox, 1)
