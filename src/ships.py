"""
Ships of the game.
"""

import random

import pygame

from utils import get_sprite


class Ship(object):
    """Base ship to make others more specialized."""

    def __init__(self, screen, image_path, bullet, speed, x, y):
        """
        Load image of the ship and set attributes.
        Store screen as well.
        """
        # load image
        self.image = pygame.image.load(image_path).convert_alpha()
        # store screen
        self.screen = screen
        # save speed
        self.speed = speed
        # store bullet
        self.bullet = bullet

        # path of the explosions images
        images_explosion_path = ["images/foo-0.png", "images/foo-1.png"]

        # get rect of image and screen
        self.rect = self.image.get_rect()
        self.screen_rect

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


    def set_bullet_position(self, go_up=False):
        """Set bullet position."""
        x, y = self.get_init_desired_bullet_pos(go_up)
        self.bullet.set_position(x, y)


    def process_bullet(self, go_up=False):
        """
        Decrease y position of bullet if it has benn fired.
        Also reset its position whether it reach out the
        top or bottom of the screen.
        """
        if self.bullet.fired:
            if go_up:
                self.bullet.decrease_y()
            else:
                self.bullet.increase_y()

            self.reset_bullet_position(go_up)
        else:
            self.set_bullet_position(go_up)


    def get_init_desired_bullet_pos(self, go_up=False):
        """Return the initial desired position of bullet."""
        if go_up:
            x = self.rect.centerx - 2
            y = self.rect.top
        else:
            x = self.rect.centerx
            y = self.rect.bottom

        return (x, y)


    def reset_bullet_position(self, go_up=False):
        """
        Reset position of bullet if it's reached out the top of screen.
        """
        if self.bullet.rect.y < self.screen_rect.top or self.bullet.rect.y > self.screen_rect.bottom:
            self.set_bullet_position(go_up)
            self.bullet.reset_fired()


    def render(self):
        """
        Render image on screen. Also render bullet if it has been fired.
        """
        if self.destroyed:
            pass
        else:
            self.screen.blit(self.image, self.rect)

            if self.bullet.fired:
                self.bullet.render()



class Ship_Player(Ship):
    """Ship that user will control."""

    def __init__(self, screen, bullet):
        """Set attributes up and set initial position."""
        image_path = "images/ship.png"
        # get screen's rect
        self.screen_rect = screen.get_rect()

        speed = 5

        # set at the middle bottom of screen
        x = self.screen_rect.centerx - 40
        y = self.screen_rect.bottom - 67

        # call superclass to initialize ship
        super(self.__class__, self).__init__(screen, image_path, bullet, speed, x, y)

        # set initial position of bullet
        self.set_bullet_position(go_up=True)

        # stay at initial postion at the beginning
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False



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
        elif event.key == pygame.K_SPACE:
            self.bullet.shoot()


    def keep_moving(self):
        """Keep moving."""
        if self.moving_up and not self.rect.y < self.screen_rect.top:
            self.go_up()
        elif self.moving_down and not self.rect.y > self.screen_rect.bottom - 63:
            self.go_down()
        elif self.moving_left and not self.rect.x < self.screen_rect.left:
            self.go_left()
        elif self.moving_right and not self.rect.x > self.screen_rect.right - 59:
            self.go_right()



class Ship_AI_Enemy(Ship):
    """Enemy ship with some AI."""

    def __init__(self, screen, bullet):
        pass
