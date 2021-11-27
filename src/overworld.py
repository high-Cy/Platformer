import pygame, sys
from src.level_data import levels
from src.utility import load_images
from src.background import Sky
from src.constants import *
from src.ui import UI


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, is_available, icon_speed, path):
        super().__init__()
        self.animation_list = load_images(path)
        self.frame_index = 0
        self.image = self.animation_list[self.frame_index]
        self.is_available = True if is_available else False

        self.rect = self.image.get_rect(center=pos)

        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2),
                                          self.rect.centery - (icon_speed / 2),
                                          icon_speed, icon_speed)
        self.current_time = pygame.time.get_ticks()

    def animate(self):
        self.image = self.animation_list[self.frame_index]
        if (pygame.time.get_ticks() - self.current_time) > \
                TILE_ANI:
            self.current_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def update(self):
        if self.is_available:
            self.animate()
        else:
            tint_surf = self.image.copy()
            tint_surf.fill('black', None, special_flags=pygame.BLEND_RGB_MULT)
            self.image.blit(tint_surf, (0,0))


class OverworldIcon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.transform.scale2x(
            pygame.image.load('assets/player/player_idle/idle-1.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.flip = False

    def update(self, screen):
        self.rect.center = self.pos

        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, self.rect)


class Overworld:
    def __init__(self, start_level, max_level, screen, create_level, overworld_bg):
        self.screen = screen
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level
        self.overworld_bg = overworld_bg
        self.bg_playing = True

        # UI
        self.ui = UI(self.screen)

        self.moving = False
        self.move_direction = pygame.Vector2(0, 0)
        self.speed = 8

        self.nodes = pygame.sprite.Group()
        self.setup_nodes()

        self.icon = pygame.sprite.GroupSingle()
        self.setup_icon()

        self.sky = Sky(SKY_HORIZON)

        self.start_time = pygame.time.get_ticks()
        self.allow_input = False

    def setup_nodes(self):
        for i, node in enumerate(levels.values()):
            if i <= self.max_level:
                node_sprite = Node(node['node_pos'], True, self.speed,
                                   node['node_graphics'])
            else:
                node_sprite = Node(node['node_pos'], False, self.speed,
                                   node['node_graphics'])

            self.nodes.add(node_sprite)

    def setup_icon(self):
        icon_sprite = OverworldIcon(
            self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input_timer(self):
        if not self.allow_input:
            if pygame.time.get_ticks() - self.start_time >= OVERWORLD_TIMER:
                self.allow_input = True

    def draw_path(self):
        if self.max_level > 0:
            points = [node['node_pos'] for i, node in enumerate(levels.values())
                      if i <= self.max_level]
            pygame.draw.lines(self.screen, '#a04f45', False, points, 6)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if not self.moving and self.allow_input:
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and \
                    self.current_level < self.max_level:
                self.move_direction = self.get_movement_data(is_next=True)
                self.current_level += 1
                self.moving = True
                self.icon.sprite.flip = False

            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and \
                    self.current_level > 0:
                self.move_direction = self.get_movement_data(is_next=False)
                self.current_level -= 1
                self.moving = True
                self.icon.sprite.flip = True

            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_m] and self.bg_playing:
            self.overworld_bg.stop()
            self.bg_playing = False

        if keys[pygame.K_n] and not self.bg_playing:
            self.overworld_bg.play(loops=-1)
            self.bg_playing = True

    def move_icon(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def get_movement_data(self, is_next):
        start = pygame.math.Vector2(
            self.nodes.sprites()[self.current_level].rect.center)

        if is_next:
            end = pygame.math.Vector2(
                self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(
                self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    def run(self):
        self.input_timer()
        self.get_input()
        self.move_icon()
        self.nodes.update()

        self.sky.draw(self.screen)
        self.draw_path()
        self.nodes.draw(self.screen)
        self.icon.update(self.screen)
        self.ui.display_mute()
