import pygame
from src.constants import *
from src.utility import *
from src.sword import Sword
from src.effect import Effect


class Player(pygame.sprite.Sprite):
    path = 'assets/player'

    def __init__(self, pos):
        super().__init__()
        # audio
        self.jump_sound = pygame.mixer.Sound('assets/sound/effects/jump.wav')
        self.hit_sound = pygame.mixer.Sound('assets/sound/effects/hit.wav')
        self.jump_sound.set_volume(SOUND_VOLUME)

        # animations
        self.animation_dict = {}
        self.load_images()
        self.cooldowns = {
            IDLE_IDX: IDLE_ANI, RUN_IDX: RUN_ANI,
            DEAD_IDX: DEAD_ANI, HIT_IDX: HURT_ANI,
            ATTACK_IDX: ATTACK_ANI, JUMP_IDX: JUMP_ANI
        }
        self.current_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action = IDLE_IDX
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.flip = False

        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.current_x = 0
        self.on_right = False
        self.on_left = False
        self.on_roof = False
        self.in_air = False
        self.jumped = False
        self.landed = False
        self.vel_y = 0
        self.speed = WALK_SPEED
        self.jump_vel = JUMP_VEL
        self.gravity = GRAVITY

        self.attack = False
        self.sword = Sword(self.rect.x, self.rect.y, self.flip)

        self.health = MAX_HEALTH
        self.max_health = self.health

        self.alive = True
        self.hitbox_width, self.hitbox_height = 35, 40
        self.hitbox = pygame.rect.Rect(self.rect.center, (self.hitbox_width, self.hitbox_height))

        self.tmp_hitbox = self.hitbox
        self.area = ()
        self.heart = pygame.image.load(f'{self.path}/heart.png')
        self.collided = False
        self.hurt_timer = None

        self.dust = pygame.sprite.GroupSingle()
        self.run_dust = load_images(f'{self.path}/dust_effect/run/*.png')
        self.run_frame = 0
        self.run_time = pygame.time.get_ticks()

    def load_images(self):
        # add frames to animation list
        frame_type = [IDLE_IDX, RUN_IDX, DEAD_IDX, HIT_IDX,
                      ATTACK_IDX, JUMP_IDX]
        for animation in frame_type:
            self.animation_dict[animation] = load_images(
                f'{self.path}/player_{animation}/*.png', scale=2)

    def update(self, screen, lvl_shift, collidables, enemies, muted):
        self.get_input(muted)
        self.get_action()
        self.movement(collidables)
        self.check_collision(enemies,muted)
        self.invincibility_timer()
        self.animate()
        self.draw(screen)

        if self.attack:
            self.attacking(enemies, screen, muted)

    def get_action(self):
        # Cant do anything when hurt
        if self.action != HIT_IDX and self.alive:
            if self.jumped:
                update_action(self, JUMP_IDX)
            elif self.direction.x:
                update_action(self, RUN_IDX)
            elif self.attack:
                update_action(self, ATTACK_IDX)
            else:
                update_action(self, IDLE_IDX)

        # dead
        elif not self.alive:
            update_action(self, DEAD_IDX)

    def invincibility_timer(self):
        # Grants n amount of time of invincibility after hurt
        if self.hurt_timer and (
                pygame.time.get_ticks() - self.hurt_timer) >= HURT_TIMER:
            self.hurt_timer = None
            self.collided = False

    def check_collision(self, enemy_group, muted):
        for enemy in enemy_group:
            if pygame.Rect.colliderect(self.hitbox, enemy.hitbox) and not self.attack:
                # ensure only counts 1 collision
                if enemy.alive and not self.collided and self.alive:
                    update_action(self, HIT_IDX)
                    self.collided = True
                    self.health -= 1
                    self.hurt_timer = pygame.time.get_ticks()

                    if not muted:
                        self.hit_sound.play()

                if self.health <= 0:
                    self.health = 0
                    self.direction = pygame.math.Vector2(0, 0)

    def movement(self, collidables):
        self.hitbox.x += self.direction.x * self.speed
        self.tile_collide_x(collidables)

        self.apply_gravity()
        self.tile_collide_y(collidables)

    def tile_collide_x(self, collidables):
        for sprite in collidables:
            if self.hitbox.colliderect(sprite.rect):
                if self.direction.x < 0:
                    self.hitbox.left = sprite.rect.right
                    self.on_left = True
                    self.current_x = self.hitbox.left
                elif self.direction.x > 0:
                    self.hitbox.right = sprite.rect.left
                    self.on_right = True
                    self.current_x = self.hitbox.right
                self.direction.x = 0

    def tile_collide_y(self, collidables):
        for sprite in collidables:
            if self.hitbox.colliderect(sprite.rect):
                if self.direction.y > 0:
                    self.hitbox.bottom = sprite.rect.top
                    self.jumped = False
                    if self.direction.y > 2*self.gravity:
                        self.landed = True

                elif self.direction.y < 0:
                    self.hitbox.top = sprite.rect.bottom
                    self.on_roof = True
                self.direction.y = 0

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.hitbox.y += self.direction.y

    def jumping(self):
        self.direction.y = self.jump_vel

    def attacking(self, enemies, screen,muted):
        self.sword.update(enemies, screen, self.hitbox.x, self.hitbox.y, self.flip, self.frame_index, muted)

    def get_dust(self):
        if self.action == JUMP_IDX and not self.in_air:
            self.dust.add(Effect(JUMP_IDX, self.hitbox.midbottom))
            self.in_air = True
        if not self.dust:
            # landing from jumping or falling
            if (not self.jumped and self.in_air) or self.landed:
                self.dust.add(Effect(LAND_IDX, self.hitbox.midbottom))
                self.jumped = False
                self.landed = False
                self.in_air = False

    def adjust_hitbox(self):
        self.area = (15, 15, self.hitbox.width, self.hitbox_height)
        self.tmp_hitbox = self.hitbox

        if self.attack:
            if self.flip:
                self.area = (0, 15, 64, self.hitbox_height)
                self.tmp_hitbox = (self.hitbox.left-15, self.hitbox.top, 64, self.hitbox.height)
            else:
                self.area = (15, 15, 64, self.hitbox_height)

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
            if self.action == ATTACK_IDX:
                self.attack = False
                self.sword.collided = False
                self.sword.swung = False
            elif self.action == HIT_IDX:
                self.action = IDLE_IDX
            elif self.action == DEAD_IDX:
                self.frame_index = len(
                    self.animation_dict[self.action]) - 1

        self.adjust_hitbox()

    def animate_dust(self, screen):
        if self.action == RUN_IDX:
            dust_img = pygame.transform.flip(self.run_dust[self.run_frame], self.flip, False)
            if (pygame.time.get_ticks() - self.run_time) > DUST_ANI:
                self.run_time = pygame.time.get_ticks()
                self.run_frame += 1
            if self.run_frame >= len(self.run_dust):
                self.run_frame = 0

            if self.flip:
                pos = self.hitbox.bottomright - pygame.math.Vector2(0, 10)
            else:
                pos = self.hitbox.bottomleft - pygame.math.Vector2(15, 10)

            screen.blit(dust_img, pos)

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        if self.alive:
            screen.blit(img, self.tmp_hitbox, self.area)
        else:
            screen.blit(img, self.tmp_hitbox)

        pygame.draw.rect(screen, 'red', self.hitbox, 1)

    def get_input(self, muted):
        keys = pygame.key.get_pressed()

        if self.alive:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.flip = False
                self.attack = False

            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.flip = True
                self.attack = False
            else:
                self.direction.x = 0

            if (keys[pygame.K_UP] or keys[pygame.K_w]) and not self.jumped:
                self.jumping()
                self.jumped = True
                self.attack = False
                if not muted:
                    self.jump_sound.play()

            if keys[pygame.K_SPACE]:
                self.attack = True
                self.direction.x = 0

