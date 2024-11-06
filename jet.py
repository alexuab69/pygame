import pygame
import random
from pygame.locals import RLEACCEL

from screen import Screen
from game_sprite import GameSprite

# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Jet(GameSprite):
    Max_Speed = 13
    Min_Speed = 8

    def __init__(self):
        super(Jet, self).__init__()
        self.surf = pygame.image.load("icons/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(Screen.width + 20, Screen.width + 100),
                random.randint(0, Screen.height),
            )
        )
        self.speed = random.randint(self.Min_Speed, self.Max_Speed)
        self.time = 0


    # Remove it when it passes the left edge of the screen.py
    def update(self):
        self.time += 1
        speed_x = self.speed
        speed_y = 0
        self.rect.move_ip(-speed_x, speed_y)
        if self.rect.right < 0:
            self.kill()

    def clone(self):
        # Create a new instance of Bird
        return Jet()