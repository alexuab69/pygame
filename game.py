import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from screen import Screen
from player import Player
from missile import Missile
from cloud import Cloud


class Game:
    def __init__(self):
        self._initialize_game()
        self._make_objects()
        self._load_music_and_sounds()
        self._play_music()

    def _initialize_game(self):
        # Setup for sounds_music, defaults are good
        pygame.mixer.init()
        # Initialize pygame
        pygame.init()
        # Setup the clock for a decent frame rate
        self._clock = pygame.time.Clock()
        # Create the screen object
        self._screen = pygame.display.set_mode((Screen.width, Screen.height))
        # Create custom events for adding a new missile and cloud
        new_missile_period = 250//2
        new_cloud_period = 1000//2
        # make a new missile/cloud every these milliseconds, so the smaller
        # the more new missiles/clouds
        self._add_missile = pygame.USEREVENT + 1
        pygame.time.set_timer(self._add_missile, new_missile_period)
        self._add_cloud = pygame.USEREVENT + 2
        pygame.time.set_timer(self._add_cloud, new_cloud_period)
        self._user_quits = False # to quit press Escape or close the window

    def _make_objects(self):
        # Create our 'player'
        self._player = Player()

        # Create groups to hold missile sprites, cloud sprites, and all sprites
        # - missiles is used for collision detection and position updates
        # - clouds is used for position updates
        # - all_sprites is used for rendering
        self._missiles = pygame.sprite.Group()
        self._clouds = pygame.sprite.Group()
        self._all_sprites = pygame.sprite.Group()
        self._all_sprites.add(self._player)

    @staticmethod
    def _play_music():
        pygame.mixer.music.play(loops=-1)

    def _load_music_and_sounds(self):
        # Load and play our background music
        pygame.mixer.music.load("sounds_music/Apoxode_-_Electric_1.mp3")
        self._collision_sound = pygame.mixer.Sound(
            "sounds_music/Explosion_10.ogg")
        self._collision_sound.set_volume(0.5)

    # if centers of the rectangles of the two sprites are close then there is a
    # collision. This looks better than check if the bounding boxes of the two
    # sprites intersect or not
    # TODO: make distx, disty relative to the size of the rectangles
    @staticmethod
    def _my_collide(sprite1, sprite2, distx=20, disty=10):
        pos1 = sprite1.rect.center
        pos2 = sprite2.rect.center
        return abs(pos1[0] - pos2[0]) <= distx \
            and abs(pos1[1] - pos2[1]) <= disty

    def _process_event(self):
        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop
                if event.key == K_ESCAPE:
                    self._user_quits = True
            # Did the user click the window close button? If so, stop the loop
            elif event.type == QUIT:
                self._user_quits = True
            # Should we add a new missile?
            elif event.type == self._add_missile:
                # Create the new missile, and add it to our sprite groups
                new_missile = Missile()
                self._missiles.add(new_missile)
                self._all_sprites.add(new_missile)
            # Should we add a new cloud?
            elif event.type == self._add_cloud:
                # Create the new cloud, and add it to our sprite groups
                new_cloud = Cloud()
                self._clouds.add(new_cloud)
                self._all_sprites.add(new_cloud)

    def _update(self):
        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        self._player.update(pressed_keys)
        # move the player if key was an arrow
        # Update the position of our missiles and clouds
        self._missiles.update()
        self._clouds.update()

    def _draw(self):
        # Fill the screen.py with sky blue
        self._screen.fill((135, 206, 250))
        # Draw all our sprites
        for entity in self._all_sprites:
            self._screen.blit(entity.surf, entity.rect)
        # Flip everything to the display
        pygame.display.flip()

    def _collision(self):
        return pygame.sprite.spritecollideany(self._player, self._missiles,
                                              self._my_collide)

    def _game_over(self):
        return self._collision() or self._user_quits

    def _keep_framerate(self):
        # Ensure we maintain a 30 frames per second rate
        self._clock.tick(30)

    def play(self):
        while not self._game_over():
            self._process_event()
            self._update()
            self._draw()
            self._keep_framerate()

        # Check if any missile have collided with the player
        if self._collision():
            # If so, remove the player
            self._player.kill()
            # Stop any moving sounds and play the collision sound
            self._player.stop_move_sounds()
            pygame.mixer.music.stop()
            self._collision_sound.play()
            pygame.time.wait(2000) # to play collision sound

        pygame.mixer.quit()
