"""
Ships of the game.
"""

import random

import pygame


class Ship(object):
    """Base ship to make others more specialized."""

    def __init__(self, screen, image_path, speed, x, y):
        """
        Load image of the ship and set attributes.
        Store screen as well.
        """
        # load image
        self.image = pygame.image.load(image_path)
        # store screen
        self.screen = screen
        # save speed
        self.speed = speed

        # path of the explosions images
        images_explosion_path = ["images/foo-0.png", "images/foo-1.png"]

        # stay at initial postion at the beginning
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        # get rect of image
        self.rect = self.image.get_rect()

        # set initial position
        self.rect.y = y
        self.rect.x = x

        # becase no ship will be set destroyed at
        # the start of the game
        self.destroyed = False


    def go_up(self):
        """Go upward."""
        self.rect.y -= self.speed


    def go_down(self):
        """Go downward."""
        self.rect.y += self.speed


    def go_left(self):
        """Go leftward."""
        self.rect.x -= self.speed


    def go_right(self):
        """Go rightward."""
        self.rect.x += self.speed


    def render(self):
        """Render image on screen."""
        if self.destroyed:
            pass
        else:
            self.screen.blit(self.image, self.rect)



class Ship_Player(Ship):
    """Ship that user will control."""

    def __init__(self, screen):
        """Set attributes up and set initial position."""
        image_path = "images/ship.png"
        # get screen's rect
        screen_rect = screen.get_rect()

        speed = 5

        # set position at the right of the screen
        x = screen_rect.centerx - 40
        y = screen_rect.bottom - 67

        # call superclass to initialize ship
        super(self.__class__, self).__init__(screen, image_path, speed, x, y)


    def check_keyup(self, event):
        """Check key up/down arrows events."""
        if event.key == pygame.K_UP:
            self.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.moving_down = False
        elif event.key == pygame.K_LEFT:
            self.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.moving_right = False


    def check_keydown(self, event):
        """Check key down arrows events."""
        if event.key == pygame.K_UP:
            self.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.moving_down = True
        elif event.key == pygame.K_LEFT:
            self.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.moving_right = True


    def keep_moving(self):
        """Keep moving."""
        if self.moving_up:
            self.go_up()
        elif self.moving_down:
            self.go_down()
        elif self.moving_left:
            self.go_left()
        elif self.moving_right:
            self.go_right()
