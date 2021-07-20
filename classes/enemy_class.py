import pygame
import os
import constants as c


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_list = []

        self.frame_index = 0
        self.flip = False
        self.direction = 1

    def draw(self, surf):
        img = pygame.transform.flip(self.image, self.flip, False)
        surf.blit(img, self.rect)


class Slime01(Enemy):
    def __init__(self):
        super().__init__()
        self.load_images()

        self.image = self.animation_list[0][self.frame_index]
        self.rect = self.image.get_rect(center=(300, 375))

    def load_images(self):
        frame_type = ['idle', 'move', 'hurt', 'die']
        for animation in frame_type:
            tmp_list = []
            num_frames = len(os.listdir(f'slime01/slime01-{animation}'))
            for i in range(num_frames):
                fn = f'slime01/slime01-{animation}/slime-{animation}-{i}.png'
                img = pygame.image.load(fn).convert_alpha()
                tmp_list.append(img)

            self.animation_list.append(tmp_list)

