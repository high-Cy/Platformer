import pygame
from src.constants import *
import src.tiles as t
import src.utility as u
from src.player import Player 
import src.enemy as e
import src.background as bg
from src.level_data import levels
path = 'assets/terrain'


class Level:
    def __init__(self, current_level, screen, create_overworld):
        self.screen = screen
        self.level_shift = 0

        # Overworld connection
        self.current_level = current_level
        self.create_overworld = create_overworld

        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        terrain = u.load_csv(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain, 'terrain')

        grass = u.load_csv(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass, 'grass')

        fg_palms = u.load_csv(level_data['fg palms'])
        self.fg_palms_sprites = self.create_tile_group(fg_palms, 'fg palms')

        bg_palms = u.load_csv(level_data['bg palms'])
        self.bg_palms_sprites = self.create_tile_group(bg_palms, 'bg palms')

        enemies = u.load_csv(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemies, 'enemy')

        constraints = u.load_csv(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraints, 'constraints')

        self.sky = bg.Sky(SKY_HORIZON)
        lvl_width = len(terrain[0]) * TILE_SIZE
        self.water = bg.Water(SCREEN_HEIGHT-40, lvl_width)
        self.clouds = bg.Clouds(400, lvl_width, 30)

        start_end = u.load_csv(level_data['player_startend'])
        self.player = None
        self.goal = None
        self.setup_player(start_end)

    def create_tile_group(self, layout, type):
        sprite_grp = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == 'terrain':
                        terrain_list = u.load_cut_graphics(f'{path}/terrain_tiles.png')
                        tile_surface = terrain_list[int(val)]
                        sprite = t.StaticTile( TILE_SIZE, (x, y), tile_surface)

                    if type == 'grass':
                        grass_list = u.load_cut_graphics(f'{path}/grass.png')
                        tile_surface = grass_list[int(val)]
                        sprite = t.StaticTile(TILE_SIZE, (x,y), tile_surface)

                    if type == 'fg palms':
                        if val == '1':
                            sprite = t.Palm(TILE_SIZE, (x,y), f'{path}/palm_large/*.png', 38)
                        if val == '2':
                            sprite = t.Palm(TILE_SIZE, (x,y), f'{path}/palm_small/*.png', 38)

                    if type == 'bg palms':
                        sprite = t.Palm(TILE_SIZE, (x,y), f'{path}/palm_bg/*.png', 64)

                    if type == 'enemy':
                        if val == '1':
                            sprite = e.Slime(x,y)
                        if val == '2':
                            sprite = e.Worm(x,y)

                    if type == 'constraints':
                        sprite = t.Tile(TILE_SIZE, (x,y))

                    sprite_grp.add(sprite)

        return sprite_grp

    def setup_player(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if val == '-1':
                    continue
                if val == '0':
                    self.player = Player((x,y))
                if val == '1':
                    offset = y + 35
                    end_surf = pygame.image.load(f'{path}/start_end/end.png')
                    self.goal = t.StaticTile(TILE_SIZE, (x, offset), end_surf)

    def scroll_level(self):
        player_x = self.player.hitbox.centerx
        direction_x = self.player.direction.x

        if (player_x < SCREEN_WIDTH / 4) and direction_x < 0:
            self.player.speed = 0
            self.level_shift = WALK_SPEED
        elif (player_x > SCREEN_WIDTH - (SCREEN_WIDTH / 4)) and direction_x > 0:
            self.player.speed = 0
            self.level_shift = -WALK_SPEED
        else:
            self.player.speed = WALK_SPEED
            self.level_shift = 0

    def check_death(self):
        if self.player.health <= 0 or self.player.hitbox.top > SCREEN_HEIGHT:
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.Rect.colliderect(self.player.hitbox, self.goal.rect):
            self.create_overworld(self.current_level, self.new_max_level)

    def run(self):
        self.constraint_sprites.update(self.screen, self.level_shift)
        self.scroll_level()

        self.sky.draw(self.screen)
        self.clouds.update(self.screen, self.level_shift)

        self.bg_palms_sprites.update(self.screen, self.level_shift)
        self.terrain_sprites.update(self.screen, self.level_shift)
        self.grass_sprites.update(self.screen, self.level_shift)

        collidables = self.terrain_sprites.sprites() + self.fg_palms_sprites.sprites()
        self.player.update(self.screen, self.level_shift, collidables, self.enemy_sprites)

        self.fg_palms_sprites.update(self.screen, self.level_shift)

        self.enemy_sprites.update(self.screen, self.level_shift, self.constraint_sprites)

        self.goal.update(self.screen, self.level_shift)

        self.water.update(self.screen, self.level_shift)

        self.check_death()
        self.check_win()
