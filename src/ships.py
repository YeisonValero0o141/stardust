"""
Ships of the game.
"""

import random

import pygame


class Ship:
    """Base ship to make others more specialized."""

    def __init__(self, screen, right=True):
        """
        Load image of the ship and set attributes.
        Store screen as well.
        """
        image_path = "src/ship.png"
        # load image
        self.image = pygame.image.load(image_path)
        # store screen
        self.screen = screen

        # get rect of image and screen
        self.rect = self.image.get_rect()
        screen_rect = self.screen.get_rect()

        # set initial position
        self.rect.y = self.screen_rect.centery
        if right:
            self.rect.x = screen_rect.right
        else:
            self.rect.x = screen_rect.left

        self.destroyed = False


    def render(self):
        """Render image on screen."""
        if self.destroyed:
            pass
        else:
            self.screen.blit(self.image, rect)
