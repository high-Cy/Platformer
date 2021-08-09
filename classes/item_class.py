import pygame
import constants as c


class Item(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        super().__init__()
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, screen, player):
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

        self.draw(screen)

    def draw(self, surf):
        surf.blit(self.image, self.rect)
        pygame.draw.rect(surf, 'red', self.rect, 1)


health__img = pygame.image.load('Items/health_potion.png')
doub_jump_img = pygame.image.load('Items/doub_jump_potion.png')
apple_img = pygame.image.load('Items/apple.png')
coin1_img = pygame.image.load('Items/coin1.png')
coin2_img = pygame.image.load('Items/coin2.png')
coin3_img = pygame.image.load('Items/coin3.png')
key_img = pygame.image.load('Items/key.png')

item_boxes = {
    c.HEALTH: health__img,
    c.DOUBJUMP: doub_jump_img,
    c.APPLE: apple_img,
    c.COIN1: coin1_img,
    c.COIN2: coin2_img,
    c.COIN3: coin3_img,
    c.KEY: key_img
}
