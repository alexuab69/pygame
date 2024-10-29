# gamesprite.py
import pygame

class GameSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(GameSprite, self).__init__()

    def clone(self):
        pass