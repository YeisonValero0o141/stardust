"""
Run StarDust Game.
It's a fun game.
"""

import sys

import pygame

from src.ships import Ship_Player


class Start_Dust:

    def __init__(self):
        """Set up some important things and start the game."""
        pygame.init()
        # game's title
        title = "StartDust"
        # screen's size
        self.screen_size = (900, 500)
        # open window and set title
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(title)

        self.background_color = (0, 0, 0)

        # player's ship
        self.ship = Ship_Player(self.screen)

        # frames per seconds
        self.fps = 60

        # pygame's clock
        self.clock = pygame.time.Clock()

        # run the game
        self.run()


    def run(self):
        """Run the game."""
        while True:
            # set fps
            self.clock.tick(self.fps)

            # handle events
            self.manage_events()

            # process all objects
            self.process()

            # draw all game's objects
            self.update_screen()

    def process(self):
        """
        Every objects of the game does whatever is was created to do.
        """
        self.ship.keep_moving()


    def manage_events(self):
        """
        Manage event like use closing the game, pressing the
        key arrows, etc.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.ship.check_keydown(event)
            elif event.type == pygame.KEYUP:
                self.ship.check_keyup(event)


    def update_screen(self):
        """
        Update the screen drawing all the objects of the game on it.
        """
        self.screen.fill(self.background_color)

        self.ship.render()

        pygame.display.flip()


if __name__ == "__main__":
    start_dust = Start_Dust()
