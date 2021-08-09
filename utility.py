import pygame
from pathlib import Path


def load_image(file_path, scale=None, width=None, height=None):
    img = pygame.image.load(file_path).convert_alpha()

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


def update_action(character, new_action_idx):
    if new_action_idx != character.action_index:
        character.action_index = new_action_idx
        character.frame_index = 0
        character.current_time = pygame.time.get_ticks()

