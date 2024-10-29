import pygame
import random
from pygame.locals import RLEACCEL

from game_sprite import GameSprite
from screen import Screen

class Umbrella(GameSprite):
    Min_Speed = 5
    Max_Speed = 10

    def __init__(self):
        super(Umbrella, self).__init__()
        self.surf = pygame.image.load("icons/umbrella.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, Screen.width + 20),
                -20,
            )
        )
        self.speed = random.randint(self.Min_Speed, self.Max_Speed)
        self.time = 0

    # Move the bird based on speed
    # Remove it when it passes the left edge of the screen.py
    def update(self):
        self.time += 1
        # just move the umbrella down 
        speed_x = 0
        speed_y = self.speed
        self.rect.move_ip(speed_x, speed_y)
        if self.rect.bottom < 0:
            self.kill()

    def clone(self):
        # Create a new instance of Bird
        return Umbrella()