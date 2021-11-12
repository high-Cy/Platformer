import pygame
from src.constants import *


class UI:
    def __init__(self, screen):
        self.screen = screen

        self.font30 = pygame.font.Font('lemonmilk.otf', 30)
        self.font60 = pygame.font.Font('lemonmilk.otf', 60)

        self.heart = pygame.image.load('assets/player/heart.png')
        self.score = pygame.image.load('assets/items/diamond.png')
        self.score_rect = self.score.get_rect(topleft=(50,61))

    def draw_health(self, health):
        for i in range(health):
            offset_x = 10
            self.screen.blit(self.heart, ((i * 30 + offset_x), 10))  # +100 to x if add words

    def draw_score(self, amount):
        self.screen.blit(self.score, self.score_rect)
        amount_surf = self.font30.render(str(amount), False, '#33323d')
        amount_rect = amount_surf.get_rect(midleft=(self.score_rect.right+5, self.score_rect.centery))
        self.screen.blit(amount_surf, amount_rect)

    def display_end_screen(self, cleared_level):
        if cleared_level:
            txt = self.font60.render('Level Cleared!', False, '#33323d')
        else:
            txt = self.font60.render('Game Over!', False, '#33323d')

        txt_rect = txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(txt, txt_rect)



