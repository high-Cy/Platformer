import pygame
import sys
import constants as c
from classes import player_class
from classes import  enemy_class

pygame.init()

screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption(c.CAPTION)
# pygame.display.set_icon()

clock = pygame.time.Clock()

player = player_class.Player()
slime01 = enemy_class.Slime01()

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
            if event.key == pygame.K_SPACE:
                player.attack = True

        # unpress key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.move_left = False
            if event.key == pygame.K_d:
                player.move_right = False

    screen.fill(c.BLACK)

    if player.alive:
        slime01.draw(screen)
        player.update_player(screen)


    pygame.display.update()
    clock.tick(c.FPS)
