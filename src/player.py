import pygame
from src import constants as c, utility, sword, effect

'''
ADD DEATH TIMER SO WONT RETURN TO OVERWORLD ONCE HEALTH = 0
MAYBE WAIT 3 -5 SEC BEFORE RETURNING

'''


class Player(pygame.sprite.Sprite):
    path = 'assets/player'

    def __init__(self, pos):
        super().__init__()
        # animations
        self.animation_dict = {}
        self.load_images()
        self.cooldowns = {
            c.IDLE_IDX: c.IDLE_ANI, c.RUN_IDX: c.RUN_ANI,
            c.DEAD_IDX: c.DEAD_ANI, c.HIT_IDX: c.HURT_ANI,
            c.ATTACK_IDX: c.ATTACK_ANI, c.JUMP_IDX: c.JUMP_ANI
        }
        self.current_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action = c.IDLE_IDX
        self.image = self.animation_dict[self.action][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
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
        self.speed = c.WALK_SPEED
        self.jump_vel = c.JUMP_VEL
        self.gravity = c.GRAVITY

        self.attack = False
        self.sword = sword.Sword(self.rect.x, self.rect.y, self.flip)

        self.health = c.MAX_HEALTH
        self.max_health = self.health

        self.alive = True
        self.hitbox_width, self.hitbox_height = 35, 40
        self.hitbox = pygame.rect.Rect(self.rect.x, self.rect.y, self.hitbox_width, self.hitbox_height)

        self.tmp_hitbox = self.hitbox
        self.area = ()
        self.heart = pygame.image.load(f'{self.path}/heart.png')
        self.collided = False
        self.hurt_timer = None

        self.dust = pygame.sprite.GroupSingle()
        self.run_dust = utility.load_images(f'{self.path}/dust_effect/run/*.png')
        self.run_frame = 0
        self.run_time = pygame.time.get_ticks()

    def load_images(self):
        # add frames to animation list
        frame_type = [c.IDLE_IDX, c.RUN_IDX, c.DEAD_IDX, c.HIT_IDX,
                      c.ATTACK_IDX, c.JUMP_IDX]
        for animation in frame_type:
            self.animation_dict[animation] = utility.load_images(
                f'{self.path}/player_{animation}/*.png', scale=2)

    def update(self, screen, lvl_shift, collidables, enemies):
        self.get_input()
        self.get_action()
        self.movement(collidables)
        self.check_collision(enemies)
        self.invincibility_timer()
        self.animate()
        self.draw(screen)

        self.get_dust()
        self.dust.update(lvl_shift)
        self.dust.draw(screen)
        self.animate_dust(screen)

        if self.attack:
            self.attacking(enemies, screen)

    def get_action(self):
        # Cant do anything when hurt
        if self.action != c.HIT_IDX and self.alive:
            if self.jumped:
                utility.update_action(self, c.JUMP_IDX)
            elif self.direction.x:
                utility.update_action(self, c.RUN_IDX)
            elif self.attack:
                utility.update_action(self, c.ATTACK_IDX)
            else:
                utility.update_action(self, c.IDLE_IDX)

        # dead
        elif not self.alive:
            utility.update_action(self, c.DEAD_IDX)

    def invincibility_timer(self):
        # Grants n amount of time of invincibility after hurt
        if self.hurt_timer and (
                pygame.time.get_ticks() - self.hurt_timer) >= c.HURT_TIMER:
            self.hurt_timer = None
            self.collided = False

    def check_collision(self, enemy_group):
        for enemy in enemy_group:
            if pygame.Rect.colliderect(self.hitbox, enemy.hitbox) and not self.attack:
                # ensure only counts 1 collision
                if enemy.alive and not self.collided and self.alive:
                    utility.update_action(self, c.HIT_IDX)
                    self.collided = True
                    self.health -= 1
                    self.hurt_timer = pygame.time.get_ticks()

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

    def attacking(self, enemies, screen):
        self.sword.update(enemies, screen, self.hitbox.x, self.hitbox.y, self.flip, self.frame_index)

    def get_dust(self):
        if self.action == c.JUMP_IDX and not self.in_air:
            self.dust.add(effect.Effect(c.JUMP_IDX, self.hitbox.midbottom))
            self.in_air = True
        if not self.dust:
            # landing from jumping or falling
            if (not self.jumped and self.in_air) or self.landed:
                self.dust.add(effect.Effect(c.LAND_IDX, self.hitbox.midbottom))
                self.jumped = False
                self.landed = False
                self.in_air = False

    def adjust_hitbox(self):
        if self.flip:
            self.area = (0, 15, 50, self.hitbox_height)
        else:
            self.area = (15, 15, 50, self.hitbox_height)

        if not self.attack:
            self.area = (15, 15, self.hitbox.width, self.hitbox_height)

        if self.flip and self.attack:
            self.tmp_hitbox = (self.hitbox.left-15, self.hitbox.top, self.hitbox.width,self.hitbox.height)

        else:
            self.tmp_hitbox = self.hitbox

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
                self.sword.collided = False
            elif self.action == c.HIT_IDX:
                self.action = c.IDLE_IDX
            elif self.action == c.DEAD_IDX:
                self.frame_index = len(
                    self.animation_dict[self.action]) - 1

        self.adjust_hitbox()

    def animate_dust(self, screen):
        if self.action == c.RUN_IDX:
            dust_img = pygame.transform.flip(self.run_dust[self.run_frame], self.flip, False)
            if (pygame.time.get_ticks() - self.run_time) > c.DUST_ANI:
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

        # pygame.draw.rect(screen, 'red', self.hitbox, 1)

    def get_input(self):
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

            if keys[pygame.K_SPACE]:
                self.attack = True
