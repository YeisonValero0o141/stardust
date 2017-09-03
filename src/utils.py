"""Contains some utility functions that are uses in the game."""

import pygame

def get_sprite(image, location):
    """
    Return the sprite in passed location area of image.
    Location must be passed as (x_start, y_start, x_end, y_end)
    """
    # get sprite
    image.set_clip(pygame.Rect(location))
    sprite = image.subsurface(image.get_clip())

    return sprite
