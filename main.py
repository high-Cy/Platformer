import pygame
import sys
import constants as c
from classes import player_class
from classes import  enemy_class
from classes import sword_class

pygame.init()

screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption(c.CAPTION)
# pygame.display.set_icon()

clock = pygame.time.Clock()

player = player_class.Player()
sword = sword_class.Sword(player.rect.x, player.rect.y, player.flip)

slime01 = enemy_class.Slime01(300, 375)
slime2 = enemy_class.Slime01(500, 375)
enemy_group = pygame.sprite.Group()
enemy_group.add(slime01, slime2)

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

            if event.key == pygame.K_a:
                player.move_left = True
            if event.key == pygame.K_d:
                player.move_right = True
            if event.key == pygame.K_w and not player.in_air:
                player.jump = True
                player.vel_y = 0
            # can't attack while moving
            if event.key == pygame.K_SPACE \
                    and not player.move_left and not player.move_right:
                player.attack = True

        # unpress key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.move_left = False
            if event.key == pygame.K_d:
                player.move_right = False

    screen.fill('black')

    enemy_group.update(screen)

    if player.alive:
        player.update_player(screen)

        # attack
        if player.attack and not player.move_left and not player.move_right:
            sword.update(enemy_group, screen, player.rect.x, player.rect.y, player.flip)

        else:
            player.attack = False
            sword.collided = False


    pygame.display.update()
    clock.tick(c.FPS)
