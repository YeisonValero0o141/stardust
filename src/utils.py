"""Contains some utility functions that are uses in the game."""

import time

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


def draw_msg(msg, screen, size, position=None):
    """
    Draw a message on screen. Whether position is not
    passed, it will be on the center of the screen.
    """
    if not position:
        screen_rect = screen.get_rect()
        position = [screen_rect.centerx-65, screen_rect.centery-50]

    # pygame's defaul font type
    font = pygame.font.SysFont(None, size)

    message = font.render(msg, True, (255, 255, 255), (0, 0, 0))

    rect = message.get_rect()

    # set position
    rect.x = position[0]
    rect.y = position[1]

    screen.blit(message, rect)
