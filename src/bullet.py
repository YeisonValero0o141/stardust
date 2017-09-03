"""
Bullet used by all the ships.
"""

import pygame

from utils import get_sprite


class Bullet:
    """Bullet."""

    def __init__(self, screen, image_path, location):
        """Load image that will represent bullet."""
        self.image = pygame.image.load(image_path).convert_alpha()
        self.screen = screen
        # location of the desired bullet in the image

        # get bullet
        self.image = get_sprite(self.image, location)
        # get sprite's rect
        self.rect = self.image.get_rect()

        # flag to know whether or not the bulet has been fired
        self.fired = False

        self.speed = 8

        # set initial position
        self.rect.x = 0
        self.rect.y = 0


    def set_position(self, x, y):
        """Set position according x and y."""
        self.rect.x = x
        self.rect.y = y


    def render(self):
        """Render bullet on screen."""
        self.screen.blit(self.image, self.rect)


    def shoot(self):
        """Change flag fired to True."""
        self.fired = True


    def reset_fired(self):
        """Reset fired flag to its initial Value (False)."""
        self.fired = False


    def increase_y(self):
        """Increase y position."""
        self.rect.y += self.speed


    def decrease_y(self):
        """Decrease y positino."""
        self.rect.y -= self.speed
