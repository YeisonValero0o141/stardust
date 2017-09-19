"""
Stars of the game.

Copyright: (c) 2017 by Yeison Valero.
License: MIT, see LICENSE for more information.
"""

import random

import pygame

class Star:
    """Star. It is just a whie point on screen."""

    def __init__(self, screen):
        """Store position, screen, color, and speed."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # set position and speed
        self.x = random.randint(self.screen_rect.left, self.screen_rect.right)
        self.y = random.randint(self.screen_rect.top, self.screen_rect.bottom)
        self.speed = random.randint(1, 5)

        # set color (white)
        self.color = (255, 255, 255)


    def move_down(self):
        """Move down"""
        self.y += self.speed


    def reset_y_pos(self):
        """Reset y position."""
        self.y = random.randint(self.screen_rect.top-200, self.screen_rect.top)


    def is_out_of_screen(self):
        """Check whether star has gone outside screen."""
        return self.y > self.screen_rect.bottom


    def render(self):
        """Draw a point to represent star."""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 1, 1)



class Stars:
    """All stars of the game."""

    def __init__(self, screen, numbers=150):
        """Makes stars and store them in a list."""
        self.stars = []

        for star in range(numbers):
            star = Star(screen)

            self.stars.append(star)


    def process(self):
        """Move stars down depending on their speed."""
        for star in self.stars:
            star.move_down()

            # wheter is out of screen, reset its positions
            if star.is_out_of_screen():
                star.reset_y_pos()


    def render(self):
        """Render all stars."""
        for star in self.stars:
            star.render()
