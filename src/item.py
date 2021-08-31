import pygame
from src import constants as c, utility


class Item(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        super().__init__()
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, screen, player):
        self.check_collision(player)
        self.draw(screen)

    def check_collision(self, player):
        if pygame.Rect.colliderect(self.rect, player.hitbox):
            if self.item_type == c.HEALTH and player.health < player.max_health:
                player.health = min(player.max_health, player.health + 3)

            elif self.item_type == c.DOUBJUMP:
                pass
            elif self.item_type == c.APPLE:
                pass
            elif self.item_type == c.COIN1:
                pass

            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, 'red', self.rect, 1)


path = 'assets/items'
health__img = utility.load_image(f'{path}/health_potion.png')
doub_jump_img = utility.load_image(f'{path}/doub_jump_potion.png')
apple_img = utility.load_image(f'{path}/apple.png')
coin1_img = utility.load_image(f'{path}/coin1.png')
coin2_img = utility.load_image(f'{path}/coin2.png')
coin3_img = utility.load_image(f'{path}/coin3.png')
key_img = utility.load_image(f'{path}/key.png')

item_boxes = {
    c.HEALTH: health__img,
    c.DOUBJUMP: doub_jump_img,
    c.APPLE: apple_img,
    c.COIN1: coin1_img,
    c.COIN2: coin2_img,
    c.COIN3: coin3_img,
    c.KEY: key_img
}
