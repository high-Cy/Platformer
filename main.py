import pygame
import sys
import constants as c
from classes import player
from classes import enemy
from classes import sword
from classes import item

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption(c.CAPTION)
# pygame.display.set_icon(pygame.image.load(c.ICON))

clock = pygame.time.Clock()
font = pygame.font.Font('lemonmilk.otf', 18)

player = player.Player()
sword = sword.Sword(player.rect.x, player.rect.y, player.flip)

slime01 = enemy.Slime01(300, 375)
slime2 = enemy.Slime01(500, 375)
enemy_group = pygame.sprite.Group()
enemy_group.add(slime01, slime2)

item_group = pygame.sprite.Group()
item = item.Item(c.HEALTH, 200, 375)
item_group.add(item)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # press key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if player.alive:
                if event.key == pygame.K_a:
                    player.move_left = True
                    player.attack = False

                if event.key == pygame.K_d:
                    player.move_right = True
                    player.attack = False

                if event.key == pygame.K_w and not player.in_air:
                    player.jump = True
                    player.vel_y = 0
                if event.key == pygame.K_SPACE:
                    player.attack = True

        # unpress key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.move_left = False
            if event.key == pygame.K_d:
                player.move_right = False

    screen.fill('black')

    enemy_group.update(screen, player.hitbox)

    item_group.update(screen, player)

    player.update(screen, enemy_group, font)

    if player.alive:
        # stop moving to attack
        if player.attack and not player.in_air:
            player.move_left = False
            player.move_right = False
            sword.update(enemy_group, screen, player.rect.x, player.rect.y,
                         player.flip, player.frame_index)

        else:
            player.attack = False
            sword.collided = False

    pygame.display.update()
    clock.tick(c.FPS)
