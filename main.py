import pygame
from game import Game
from screen import Screen
from factory_sprites import FactorySprites
from bird import Bird
from cloud import Cloud
from mountain import Mountain
from umbrella import Umbrella

# Initialize PyGame
# setup for sounds_music, defaults are good
pygame.mixer.init()
pygame.init()
# create the screen object
pygame.display.set_mode((Screen.width, Screen.height))

level = 'difficult'

if level=='easy':
    # easy game, only birds and clouds
    factory_flying = FactorySprites([Bird()], [300], pygame.USEREVENT + 1)
    factory_landscape = FactorySprites([Cloud()], [400], pygame.USEREVENT + 10)
elif level=='difficult':
    factory_flying = FactorySprites([Bird(), Umbrella()], [400, 500],
    pygame.USEREVENT + 1)
    factory_landscape = FactorySprites([Cloud(), Mountain()], [500, 2000,],
    pygame.USEREVENT + 10)
else:
    assert False
# start playing
game = Game(factory_flying, factory_landscape)
game.play()