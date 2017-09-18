"""
Run StarDust Game.
It's a fun game.
"""

import sys
import time

import pygame

from src.ships import Ship_Player, Ship_AI_Enemy, Fleet_Enemy
from src.stars import Stars
from src.utils import draw_msg


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

        # times to know when draw 'game over' message
        self.time_msg = time.time()
        self.time_wait_msg = time.time()

        # black
        self.background_color = (0, 0, 0)

        # background sound's path
        sound_path = "sounds/DST-AngryMod.mp3"

        # load music, set volume and play it in a loop
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)

        # flag to know whether or not the game has started
        self.running = False

        # first bullet's path and location in the image
        self.bullet1_path = "images/Bullet2.bmp"
        self.bullet1_location = (64, 1, 5, 10)

        # stars of brackground
        self.stars = Stars(self.screen)

        # frames per seconds
        self.fps = 60

        # there are just three levels
        self.level = 0

        # hide cursor
        pygame.mouse.set_visible(False)

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
        Every object of the game does whatever is was created to do.
        """
        self.stars.process()

        if self.running:
            self.ship.process(self.fleet_enemy, self.fleet_ai_enemy, self.close)
            self.fleet_enemy.process(self.ship, self.level)
            self.fleet_ai_enemy.process(self.ship, self.level, ai_ships=True)

            # if all enemies ships are destroyed:
            if not self.fleet_enemy.ships and not self.fleet_ai_enemy.ships:

                if not self.level >= 5:
                    # level up
                    self.level += 1

                if not self.level >= 5:
                    # make fleets again
                    self.fleet_enemy.make_ship(self.screen, self.bullet1_path, self.bullet1_location, level=self.level)
                    self.fleet_ai_enemy.make_ship(self.screen, self.bullet1_path, self.bullet1_location, ai_ships=True, level=self.level)
        else:
            self.reset_level()


    def manage_events(self):
        """
        Manage event like use closing the game, pressing the
        key arrows, etc.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.KEYDOWN:
                if not self.running:
                    self.start_game(event)
                else:
                    self.ship.check_keydown(event)
            elif event.type == pygame.KEYUP and self.running:
                self.ship.check_keyup(event)


    def update_screen(self):
        """
        Update the screen drawing all the objects of the game on it.
        """
        self.screen.fill(self.background_color)
        self.stars.render()

        if self.running:
            # draw 'game over' message if ship is destroyed
            if self.ship.destroyed:
                self.show_msg("Game Over", 60, (350, 180))

            # whether player has won
            if self.level >= 5:
                self.show_msg("You have won", 60, (310, 190))

            # draw level
            draw_msg("Level {}".format(self.level), self.screen, 30, (420, 0))

            # render game's objects
            self.ship.render()
            self.fleet_enemy.render()
            self.fleet_ai_enemy.render()

        else:
            draw_msg("Start", self.screen, 60)

        pygame.display.flip()

    def start_game(self, event):
        """If enter key has been pressed, start game."""
        if event.key == pygame.K_RETURN:
            self.running = True
            self.init_ships()


    def show_msg(self, msg, size, pos):
        """Draw 'Game Over' on screen for a second."""
        if self.time_msg < self.time_wait_msg:
            self.time_msg = time.time() + 3
        else:
            self.time_wait_msg = time.time()

        # draw message
        draw_msg(msg, self.screen, size, pos)

        if self.time_wait_msg >= self.time_msg:
            self.running = False


    def init_ships(self):
        """Instance all game's object."""
        # player's ship
        self.ship = Ship_Player(self.screen, self.bullet1_path, self.bullet1_location)
        # enemy fleet
        self.fleet_enemy = Fleet_Enemy(self.screen, self.bullet1_path, self.bullet1_location)
        # ai enemy fleet
        self.fleet_ai_enemy = Fleet_Enemy(self.screen, self.bullet1_path, self.bullet1_location, ai_ships=True)


    def reset_level(self):
        """Set level to its initial value."""
        self.level = 0


    def close(self):
        """Close game."""
        pygame.quit()
        sys.exit()



if __name__ == "__main__":
    start_dust = Start_Dust()
