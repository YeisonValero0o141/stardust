"""
Run StarDust Game.
It's a fun game.
"""

import sys

import pygame

from src.ships import Ship_Player, Ship_AI_Enemy, Fleet_Enemy
from src.bullet import Bullet


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

        # black
        self.background_color = (0, 0, 0)

        # background sound's path
        sound_path = "sounds/DST-AngryMod.mp3"

        # load music, set volume and play it in loop
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)


        # first bullet's path and location in the image
        self.bullet1_path = "images/Bullet2.bmp"
        self.bullet1_location = (64, 1, 5, 10)

        # player's ship
        self.ship = Ship_Player(self.screen, self.bullet1_path, self.bullet1_location)
        # enemy fleet
        self.fleet_enemy = Fleet_Enemy(self.screen, self.bullet1_path, self.bullet1_location)
        # ai anemy fleet
        self.fleet_ai_enemy = Fleet_Enemy(self.screen, self.bullet1_path, self.bullet1_location, ai_ships=True)

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
        self.ship.process(self.fleet_enemy, self.fleet_ai_enemy, self.close)
        self.fleet_enemy.process(self.ship, self.level)
        self.fleet_ai_enemy.process(self.ship, self.level, ai_ships=True)

        # if all enemies ships are destroyed:
        if not self.fleet_enemy.ships and not self.fleet_ai_enemy.ships:
            # level up
            self.level += 1

            self.fleet_enemy.make_ship(self.screen, self.bullet1_path, self.bullet1_location, level=self.level)
            self.fleet_ai_enemy.make_ship(self.screen, self.bullet1_path, self.bullet1_location, ai_ships=True, level=self.level)



    def manage_events(self):
        """
        Manage event like use closing the game, pressing the
        key arrows, etc.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
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

        self.fleet_enemy.render()
        self.fleet_ai_enemy.render()

        pygame.display.flip()


    def close(self):
        """Close game."""
        pygame.quit()
        sys.exit()



if __name__ == "__main__":
    start_dust = Start_Dust()
