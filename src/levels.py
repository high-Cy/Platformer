import pygame
from src import constants as c
from src import tiles
from src import utility as u
from src import player
from src import enemy
from src import background as bg

path = 'assets/terrain'


class Level:
    def __init__(self, level_data, surface):
        self.screen = surface

        terrain = u.load_csv(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain, 'terrain')

        grass = u.load_csv(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass, 'grass')

        fg_palms = u.load_csv(level_data['fg palms'])
        self.fg_palms_sprites = self.create_tile_group(fg_palms, 'fg palms')

        enemies = u.load_csv(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemies, 'enemy')

        constraints =  u.load_csv(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraints, 'constraints')

        self.sky = bg.Sky(5)
        lvl_width = len(terrain[0]) * c.TILE_SIZE
        self.water = bg.Water(c.SCREEN_HEIGHT-40, lvl_width)
        self.clouds = bg.Clouds(400, lvl_width, 30)

        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.setup_level(level_data)

        self.level_shift = -5

    def create_tile_group(self, layout, type):
        sprite_grp = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * c.TILE_SIZE
                    y = row_index * c.TILE_SIZE

                    if type == 'terrain':
                        terrain_list = u.load_cut_graphics(f'{path}/terrain_tiles.png')
                        tile_surface = terrain_list[int(val)]
                        sprite = tiles.StaticTile(c.TILE_SIZE, (x, y), tile_surface)

                    if type == 'grass':
                        grass_list = u.load_cut_graphics(f'{path}/grass.png')
                        tile_surface = grass_list[int(val)]
                        sprite = tiles.StaticTile(c.TILE_SIZE, (x,y), tile_surface)

                    if type == 'fg palms':
                        if val == '1':
                            sprite = tiles.Palm(c.TILE_SIZE, (x,y), f'{path}/palm_large/*.png', 38)
                        if val == '2':
                            sprite = tiles.Palm(c.TILE_SIZE, (x,y), f'{path}/palm_small/*.png', 38)

                    if type == 'enemy':
                        if val == '1':
                            sprite = enemy.Slime(x,y)
                        if val == '2':
                            sprite = enemy.Worm(x,y)

                    if type == 'constraints':
                        sprite = tiles.Tile(c.TILE_SIZE, (x,y))

                    sprite_grp.add(sprite)

        return sprite_grp

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * c.TILE_SIZE
                y = row_index * c.TILE_SIZE

                if cell == 'X':
                    tile = tiles.Tile((x, y), c.TILE_SIZE)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = player.Player((x, y))
                    self.player.add(player_sprite)

    def scroll_level(self):
        player = self.player.sprite
        player_x = player.hitbox.centerx
        direction_x = player.direction.x

        if (player_x < c.SCREEN_WIDTH / 4) and direction_x < 0:
            player.speed = 0
            self.level_shift = c.WALK_SPEED
        elif (player_x > c.SCREEN_WIDTH - (c.SCREEN_WIDTH / 4)) and direction_x > 0:
            player.speed = 0
            self.level_shift = -c.WALK_SPEED
        else:
            player.speed = c.WALK_SPEED
            self.level_shift = 0

    def run(self):
        self.constraint_sprites.update(self.screen, self.level_shift)
        # self.scroll_level()

        self.sky.draw(self.screen)
        self.clouds.update(self.screen, self.level_shift)

        self.player.update(self.screen, self.tiles, self.level_shift)

        self.terrain_sprites.update(self.screen, self.level_shift)

        self.grass_sprites.update(self.screen, self.level_shift)

        self.fg_palms_sprites.update(self.screen, self.level_shift)

        self.enemy_sprites.update(self.screen, self.level_shift, self.constraint_sprites)
