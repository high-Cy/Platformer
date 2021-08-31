import pygame
from csv import reader
from pathlib import Path
from src import constants as c


def load_image(file_path, scale=None, width=None, height=None):
    img = pygame.image.load(file_path)  # .convert_alpha()

    if width is None:
        width = img.get_width()
    if height is None:
        height = img.get_height()

    if scale is not None:
        width = int(width * scale)
        height = int(height * scale)

    img = pygame.transform.scale(img, (width, height))

    return img


def load_images(glob, scale=None, width=None, height=None):
    def convert_to_int(path):
        # Extract any digits from the name and convert to an int
        name = path.stem
        digits = [d for d in name if d.isdigit()]
        return int("".join(digits))

    image_files = Path(".").glob(glob)
    # Sort by name as integer
    image_files = sorted(image_files, key=convert_to_int)

    # Load and scale images
    images = [
        load_image(file_path, scale=scale, width=width, height=height)
        for file_path in image_files
    ]

    return images


def load_csv(path):
    layout = []
    with open(path) as f:
        level = reader(f, delimiter=',')
        for row in level:
            layout.append(list(row))
    return layout


def load_cut_graphics(path):
    img = pygame.image.load(path)
    tile_num_x = int(img.get_size()[0] / c.TILE_SIZE)
    tile_num_y = int(img.get_size()[1] / c.TILE_SIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * c.TILE_SIZE
            y = row * c.TILE_SIZE

            new_surf = pygame.Surface((c.TILE_SIZE, c.TILE_SIZE), flags=pygame.SRCALPHA)
            new_surf.blit(img, (0, 0),
                          pygame.Rect(x, y, c.TILE_SIZE, c.TILE_SIZE))

            cut_tiles.append(new_surf)

    return cut_tiles


def update_action(character, new_action):
    if new_action != character.action:
        character.action = new_action
        character.frame_index = 0
        character.current_time = pygame.time.get_ticks()
