import pygame
from src.constants import *
import src.tiles as t
import src.utility as u
from src.player import Player
import src.enemy as e
import src.background as bg
from src.level_data import levels
from src.tiles import Item
from src.ui import UI

path = 'assets/terrain'

'''ADD NUMBER OF ENEMIES KILLED AND DISPLAY AT END SCREEN
ALSO DISPLAY SCORE NOOB'''

class Level:
    def __init__(self, current_level, screen, create_overworld, level_bg):
        self.screen = screen
        self.level_shift = 0
        self.score = 0

        # UI
        self.ui = UI(self.screen)

        # Overworld connection
        self.current_level = current_level
        self.create_overworld = create_overworld

        # Audio
        self.level_bg = level_bg
        self.coin_sound = pygame.mixer.Sound('assets/sound/effects/coin.wav')
        self.potion_sound = pygame.mixer.Sound('assets/sound/effects/potion.wav')
        self.death_sound = pygame.mixer.Sound('assets/sound/effects/oof.mp3')
        self.coin_sound.set_volume(SOUND_VOLUME)
        self.potion_sound.set_volume(SOUND_VOLUME)


        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        # World
        terrain = u.load_csv(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain, 'terrain')
        grass = u.load_csv(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass, 'grass')
        fg_palms = u.load_csv(level_data['fg palms'])
        self.fg_palms_sprites = self.create_tile_group(fg_palms, 'fg palms')
        bg_palms = u.load_csv(level_data['bg palms'])
        self.bg_palms_sprites = self.create_tile_group(bg_palms, 'bg palms')
        items = u.load_csv(level_data['items'])
        self.items_sprites = self.create_tile_group(items, 'items')
        enemies = u.load_csv(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemies, 'enemy')
        constraints = u.load_csv(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraints,
                                                         'constraints')

        # Background
        self.sky = bg.Sky(SKY_HORIZON)
        lvl_width = len(terrain[0]) * TILE_SIZE
        self.water = bg.Water(SCREEN_HEIGHT - 40, lvl_width)
        self.clouds = bg.Clouds(400, lvl_width, 30)

        start_end = u.load_csv(level_data['player_startend'])
        self.player = None
        self.goal = None
        self.setup_player(start_end)

        self.end_screen_timer = None
        self.cleared_level = None

    def create_tile_group(self, layout, type):
        sprite_grp = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == 'terrain':
                        terrain_list = u.load_cut_graphics(
                            f'{path}/terrain_tiles.png')
                        tile_surface = terrain_list[int(val)]
                        sprite = t.StaticTile(TILE_SIZE, (x, y), tile_surface)

                    if type == 'grass':
                        grass_list = u.load_cut_graphics(f'{path}/grass.png')
                        tile_surface = grass_list[int(val)]
                        sprite = t.StaticTile(TILE_SIZE, (x, y), tile_surface)

                    if type == 'fg palms':
                        if val == '1':
                            sprite = t.Palm(TILE_SIZE, (x, y),
                                            f'{path}/palm_large/*.png', 38)
                        if val == '2':
                            sprite = t.Palm(TILE_SIZE, (x, y),
                                            f'{path}/palm_small/*.png', 38)

                    if type == 'bg palms':
                        sprite = t.Palm(TILE_SIZE, (x, y),
                                        f'{path}/palm_bg/*.png', 64)

                    if type == 'items':
                        offset_x = 10
                        offset_y = 20
                        if val == '0':
                            surf = pygame.image.load('assets/items/diamond.png')
                            sprite = Item(TILE_SIZE, DIAMOND1,
                                          (x + offset_x, y + offset_y), surf)
                        if val == '1':
                            surf = pygame.image.load(
                                'assets/items/diamond2.png')
                            sprite = Item(TILE_SIZE, DIAMOND2,
                                          (x + offset_x, y + offset_y), surf)
                        if val == '2':
                            surf = pygame.image.load(
                                'assets/items/health_potion.png')
                            sprite = Item(TILE_SIZE, HEALTH_POTION,
                                          (x + offset_x, y + offset_y), surf)

                    if type == 'enemy':
                        if val == '1':
                            sprite = e.Slime(x, y)
                        if val == '2':
                            sprite = e.Worm(x, y)

                    if type == 'constraints':
                        sprite = t.Tile(TILE_SIZE, (x, y))

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
                    self.player = Player((x, y))
                if val == '1':
                    offset = y + 35
                    end_surf = pygame.image.load(f'{path}/start_end/end.png')
                    self.goal = t.StaticTile(TILE_SIZE, (x, offset), end_surf)

    def update_player_dust(self):
        self.player.get_dust()
        self.player.dust.update(self.level_shift)
        self.player.dust.draw(self.screen)
        self.player.animate_dust(self.screen)

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

    def check_item_collision(self):
        for item in self.items_sprites:
            if pygame.Rect.colliderect(self.player.hitbox, item.rect):
                if item.item_type == DIAMOND1:
                    self.score += D1_SCORE
                    self.coin_sound.play()

                elif item.item_type == DIAMOND2:
                    self.score += D2_SCORE
                    self.coin_sound.play()

                elif item.item_type == HEALTH_POTION:
                    self.player.health = min(self.player.health+ HEAL_AMOUNT, MAX_HEALTH)
                    self.potion_sound.play()

                item.kill()

    def check_win_lose(self):
        # timer starts when win or lose detected,
        if not self.end_screen_timer:
            if self.player.health <= 0 or self.player.hitbox.top > SCREEN_HEIGHT:
                self.death_sound.play()
                self.cleared_level = False
                self.player.alive = False
                self.end_screen_timer = pygame.time.get_ticks()
                self.level_bg.stop()

            elif pygame.Rect.colliderect(self.player.hitbox, self.goal.rect):
                self.cleared_level = True
                self.end_screen_timer = pygame.time.get_ticks()

    def end_screen(self):
        # display end screen
        if self.end_screen_timer:
            if (pygame.time.get_ticks() - self.end_screen_timer) >= ENDSCREEN_TIMER:
                if self.cleared_level:
                    self.create_overworld(self.current_level, self.new_max_level)
                else:
                    self.create_overworld(self.current_level, 0)
            else:
                self.ui.display_end_screen(self.cleared_level)

    def run(self):
        self.scroll_level()
        self.constraint_sprites.update(self.screen, self.level_shift)
        self.sky.draw(self.screen)
        self.clouds.update(self.screen, self.level_shift)

        if self.player.alive and not self.cleared_level:
            self.bg_palms_sprites.update(self.screen, self.level_shift)
            self.update_player_dust()
            self.terrain_sprites.update(self.screen, self.level_shift)
            self.grass_sprites.update(self.screen, self.level_shift)
            self.items_sprites.update(self.screen, self.level_shift)
            self.enemy_sprites.update(self.screen, self.level_shift,
                                      self.constraint_sprites)
            self.fg_palms_sprites.update(self.screen, self.level_shift)
            self.goal.update(self.screen, self.level_shift)
            self.water.update(self.screen, self.level_shift)

            self.ui.draw_health(self.player.health)
            self.ui.draw_score(self.score)

            self.check_item_collision()
            self.check_win_lose()

        collidables = self.terrain_sprites.sprites() + self.fg_palms_sprites.sprites()
        self.player.update(self.screen, self.level_shift, collidables,
                           self.enemy_sprites)

        self.end_screen()

