import pygame
import utility
import constants as c

class Effect:
    def __init__(self, type):
        self.animation_dict = {}
        if type == c.JUMP_IDX:
            path = 'assets'
