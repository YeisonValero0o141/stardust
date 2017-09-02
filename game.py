"""
Run StarDust Game.
It's a fun game.
"""

import sys

import pygame


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

        # run the game
        self.run()


    def run(self):
        """Run the game."""
        while True:
            # handle events
            self.manage_events()

            # draw all game's objects
            self.update_screen()


    def manage_events(self):
        """
        Manage event like use closing the game, pressing the
        key arrows, etc.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()


    def update_screen(self):
        """
        Update the screen drawing all the objects of the game on it.
        """
        self.screen.fill(self.background_color)
        pygame.display.flip()


if __name__ == "__main__":
    start_dust = Start_Dust()
