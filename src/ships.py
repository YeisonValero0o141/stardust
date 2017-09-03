"""
Ships of the game.
"""

import random

import pygame

from bullet import Bullet
from utils import get_sprite


class Ship(object):
    """Base ship to make others more specialized."""

    def __init__(self, screen, image, bullet, speed, x, y):
        """
        Load image of the ship and set attributes.
        Store screen as well.
        """
        # load image
        self.image = image
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
        self.screen_rect = self.screen.get_rect()

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

    def __init__(self, screen, bullet_path, bullet_location):
        """Set attributes up and set initial position."""
        image_path = "images/ship.png"
        # load image
        self.image = pygame.image.load(image_path).convert_alpha()

        # instance bullet
        self.bullet = Bullet(screen, bullet_path, bullet_location)

        # get screen's rect
        screen_rect = screen.get_rect()

        speed = 5

        # set position at the middle bottom of screen
        x = screen_rect.centerx - 40
        y = screen_rect.bottom - 67

        # call superclass to initialize ship
        super(self.__class__, self).__init__(screen, self.image, self.bullet, speed, x, y)

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

    def __init__(self, screen, bullet_path, bullet_location):
        """Set position and turn image."""
        image_path = "images/ship.png"
        self.image = pygame.image.load(image_path).convert_alpha()

        # rotate image
        self.image = pygame.transform.rotate(self.image, 180)

        # get screen's rect
        screen_rect = screen.get_rect()

        # set position at the middle top of screen
        x = screen_rect.centerx - 40
        y = screen_rect.top

        speed = 2

        # instance bullet
        self.bullet = Bullet(screen, bullet_path, bullet_location)

        # class superclass to initialize ship
        super(self.__class__, self).__init__(screen, self.image, self.bullet, speed, x, y)

        # set initial position of bullet
        self.set_bullet_position()

        # set default state machine. There are just two possibles states exploring and destroying
        self.state = "exploring"
        # flag to know whether or not it has reach out the destination
        self.has_come_dest = False

        # minimum distance to swtich to destroying state
        self.min_x_distance = 20
        self.min_y_distance = 450

        # at the beginning the destination is the initial
        # position but this will change
        self.x_dest = self.rect.x
        self.y_dest = self.rect.y


    def get_distance_to(self, ship):
        """Return the distance that separate it with ship."""
        distance_x = self.rect.x - ship.rect.x
        distance_y = self.rect.y - ship.rect.y

        return (distance_x, distance_y)


    def can_see(self, ship):
        """Wheter it can see ship, switch to destroying."""
        distance = self.get_distance_to(ship)
        if distance[0] < self.min_x_distance and distance[1] < self.min_y_distance:
            self.state = "destroying"
        else:
            self.state = "exploring"


    def set_destination(self):
        """Set destination randomly."""
        # get the positions available by speed
        x_space_avail = range(self.screen_rect.left, self.screen_rect.right-53, self.speed)
        y_space_avail = range(self.screen_rect.top, self.screen_rect.bottom-63, self.speed)

        # set new position of one of the options
        self.x_dest = random.choice(x_space_avail)
        self.y_dest = random.choice(y_space_avail)


    def process(self, ship):
        """Process all actions."""
        # set which one of the two state is appropiate
        self.can_see(ship)

        if self.state == "exploring":
            self.explore()
        else:
            self.destroy(ship)


    def can_shoot_to(self, ship):
        """Shoot if it is in front of the ship."""
        if self.rect.x == ship.rect.x and self.rect.y < ship.rect.y:
            return True
        else:
            return False


    def destroy(self, ship):
        """Try to destroy ship."""
        # if ship is in front, shoot it
        if self.can_shoot_to(ship):
            self.bullet.shoot()
        else:
            # if not, try to get to ship
            self.move_x(ship.rect.x)
            self.move_y(ship.rect.y)


    def explore(self):
        """Move around screen until find the ship."""
        # wheter it already has come to destination
        if self.has_come_to_dest():
            # set new destination
            self.set_destination()

        # if not, just keep moving until get to destination
        self.move_x(self.x_dest)
        self.move_y(self.y_dest)



    def has_come_to_dest(self):
        """"Check it it has come to destination. Return bool."""
        if self.rect.x == self.x_dest and self.rect.y == self.y_dest:
            return True
        else:
            return False


    def move_x(self, target):
        """Move right or left to get to x dest."""
        if self.rect.x < target:
            self.go_right()
        elif self.rect.x > target:
            self.go_left()


    def move_y(self, target):
        """Move up or down to get to y dest."""
        if self.rect.y < target:
            self.go_down()
        elif self.rect.y > target:
            self.go_up()
