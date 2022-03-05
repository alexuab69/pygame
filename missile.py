import pygame
import random
from pygame.locals import RLEACCEL

from screen import Screen


# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super(Missile, self).__init__()
        self.surf = pygame.image.load("icons/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(Screen.width + 20, Screen.width + 100),
                random.randint(0, Screen.height),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen.py
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()