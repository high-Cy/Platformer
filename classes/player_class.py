import pygame
import os
import constants as c
import utility


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # frames
        self.animation_dict = {}
        self.load_images()

        # animations
        self.cooldowns = {
            c.IDLE_IDX: c.IDLE_ANI, c.MOVE_IDX: c.RUN_ANI,
            c.DEAD_IDX: c.DEAD_ANI, c.HURT_IDX: c.HURT_ANI,
            c.ATTACK_IDX: c.ATTACK_ANI, c.JUMP_IDX: c.JUMP_ANI
        }
        self.current_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action = c.IDLE_IDX
        self.image = self.animation_dict[self.action][self.frame_index]
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

        self.health = c.MAX_HEALTH
        self.max_health = self.health

        self.alive = True
        self.hitbox = pygame.Rect(self.rect.x + 11, self.rect.y + 15, 29, 39)
        self.heart = pygame.image.load('player/heart.png')
        self.collided = False
        self.hurt_timer = None

    def load_images(self):
        # add frames to animation list
        frame_type = [c.IDLE_IDX, c.MOVE_IDX, c.DEAD_IDX, c.HURT_IDX,
                      c.ATTACK_IDX]
        for animation in frame_type:
            self.animation_dict[animation] = utility.load_images(
                f'player/player_{animation}/*.png', scale=2)

        # jumping only has one frame
        self.animation_dict[c.JUMP_IDX] = [utility.load_image(
            'player/player_jump.png', scale=2)]

    def update(self, screen, enemy_group, font):
        # Cant do anything when hurt
        if self.action != c.HURT_IDX and self.alive:
            if self.in_air:
                utility.update_action(self, c.JUMP_IDX)
            elif self.move_left or self.move_right:
                utility.update_action(self, c.MOVE_IDX)
            elif self.attack:
                utility.update_action(self, c.ATTACK_IDX)
            else:
                utility.update_action(self, c.IDLE_IDX)
            # can't move if hurt
            self.move()
            self.check_collision(enemy_group)

        # dead
        elif not self.alive:
            utility.update_action(self, c.DEAD_IDX)

        # Grants n amount of time of invincibility after hurt
        if self.hurt_timer and (
                pygame.time.get_ticks() - self.hurt_timer) >= c.HURT_TIMER:
            self.hurt_timer = None
            self.collided = False

        self.animate()
        self.draw(screen)

        self.draw_health(screen, font)

    def check_collision(self, enemy_group):
        for enemy in enemy_group:
            if pygame.Rect.colliderect(self.hitbox, enemy.hitbox):
                # ensure only counts 1 collision
                if enemy.alive and not self.collided:
                    utility.update_action(self, c.HURT_IDX)
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
            self.vel_y = self.jump_vel
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
        self.image = self.animation_dict[self.action][self.frame_index]
        if (pygame.time.get_ticks() - self.current_time) > \
                self.cooldowns[self.action]:
            self.current_time = pygame.time.get_ticks()
            self.frame_index += 1

        # reset frame index
        if self.frame_index >= len(self.animation_dict[self.action]):
            self.frame_index = 0
            # only play player_attack animation once per key pressed
            if self.action == c.ATTACK_IDX:
                self.attack = False
            elif self.action == c.HURT_IDX:
                self.action = c.IDLE_IDX
            elif self.action == c.DEAD_IDX:
                self.frame_index = len(
                    self.animation_dict[self.action]) - 1

    def draw_health(self, screen, font):
        # surf = font.render('Health: ', True, 'white')
        # screen.blit(surf, (20, 20))
        for i in range(self.health):
            screen.blit(self.heart, ((i * 30), 5))  # +100 to x if add words

    def draw(self, surf):
        img = pygame.transform.flip(self.image, self.flip, False)
        surf.blit(img, self.rect)

        # adjust hitbox
        self.hitbox = pygame.Rect(self.rect.x + 22, self.rect.y + 15, 29, 39) \
            if self.flip else \
            pygame.Rect(self.rect.x + 11, self.rect.y + 15, 29, 39)
        pygame.draw.rect(surf, 'red', self.hitbox, 1)
