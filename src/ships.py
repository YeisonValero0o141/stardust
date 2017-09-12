"""
Ships of the game.
"""

import random
import time

import pygame

from bullet import Bullet
from utils import get_sprite


class Ship(object):
    """Base ship to make others more specialized."""

    def __init__(self, screen, image, bullet, speed, x, y, id_ship=None):
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

        # sprites of explosions
        self.explosions_sprites = self.get_sprites_exploding()

        # will be used like index to render all explosion's sprites
        self.count = 0

        # get rect of image and screen
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # set initial position
        self.rect.y = y
        self.rect.x = x

        # becase no ship will be set destroyed at
        # the start of the game
        self.destroyed = False
        # flag to know when update time_after_shot
        self.update_time_after_shot = True

        # ships' id
        self.id = id_ship

        # flag to know when pass the id to dead_ships list of Fleet_Enemy
        self.pass_id = False

        # ships won't can move when they are destroyed
        self.dont_move = False

        self.time_after_shot = time.time()
        self.time_before_shot = time.time()


    def get_sprites_exploding(self):
        """Return the sprites of explosions."""
        # path of the explosions images
        images_explosion_path = ["images/foo-0.png", "images/foo-1.png"]
        # that sprites are in two different images
        image1 = pygame.image.load(images_explosion_path[0])
        image2 = pygame.image.load(images_explosion_path[1])

        # locations of all spirtes in images
        location = [
            (0, 0, 25, 30), (25, 0, 45, 40),
            (70, 0, 40, 65), (110, 0, 32, 80),
            (140, 0, 40, 80), (178, 0, 54, 90),
            [0, 0, 35, 80]
        ]

        # will contain all sprites
        sprites = []

        # get exploding sprites
        sprite1 = get_sprite(image1, location[0])
        sprite2 = get_sprite(image1, location[1])
        sprite3 = get_sprite(image1, location[2])
        sprite4 = get_sprite(image1, location[3])
        sprite5 = get_sprite(image1, location[4])
        sprite6 = get_sprite(image1, location[5])

        # add sprites of 1st image
        sprites.append(sprite1)
        sprites.append(sprite2)
        sprites.append(sprite3)
        sprites.append(sprite4)
        sprites.append(sprite5)
        sprites.append(sprite6)

        # add sprites of the second one
        for x in range(6):
            sprite = get_sprite(image2, location[6])
            # increase x axis positions to can get the next sprite
            location[6][0] += 36

            sprites.append(sprite)

        return sprites


    def go_up(self):
        """Go upward if ship can move."""
        if not self.dont_move:
            self.rect.y -= self.speed


    def go_down(self):
        """Go downward if ship can move."""
        if not self.dont_move:
            self.rect.y += self.speed


    def go_left(self):
        """Go leftward if ship can move."""
        if not self.dont_move:
            self.rect.x -= self.speed


    def go_right(self):
        """Go rightward if ship can move."""
        if not self.dont_move:
            self.rect.x += self.speed



    def has_been_shot(self, bullet):
        """Wheter it has been shot, change destroyed to True."""
        if bullet.rect.colliderect(self.rect) and bullet.fired:
            self.destroyed = True


    def collide_with(self, ship):
        """If it collide with ship switch destroyed to True."""
        if ship.rect.colliderect(self.rect) and not self.destroyed:
            # change its own value to draw exploding sprites and stop moving
            self.destroyed = True
            self.dont_move = True

            # same thing here, but with the ship player
            ship.destroyed = True
            ship.dont_move = True


    def pass_id_to_dead_ships(self, dead_ships):
        """
        Pass the id of the ship to dead_ships list
        whether ship is destroyed or out of screen.
        """
        if self.destroyed and self.pass_id or \
        self.rect.y > self.screen_rect.bottom:
            if not self.id in dead_ships:
                dead_ships.append(self.id)


    def has_been_shot_by_fleet(self, fleet):
        """Check if it has been shot."""
        for ship in fleet.ships.values():
            if ship.bullet.rect.colliderect(self.rect) and ship.bullet.fired:
                self.destroyed = True


    def process(self, ship_player=None, go_up=False,  fleet_1=[], fleet_2=[]):
        """Do actions of ship."""
        if not ship_player:
            self.has_been_shot_by_fleet(fleet_1)
            self.has_been_shot_by_fleet(fleet_2)
        else:
            self.has_been_shot(ship_player.bullet)

        if self.destroyed:
            self.dont_move = True

            # it will not be draw bullet because it has destroyed ship
            if ship_player:
                ship_player.bullet.reset_fired()
                ship_player.set_bullet_position()
            else:
                self.bullet.reset_fired()
                self.set_bullet_position(go_up)

            # to avoid update time_after_shot over and over again
            if self.update_time_after_shot:
                # update time plus a mili seconds
                self.time_after_shot = time.time() + 0.1
                self.update_time_after_shot = False

        self.process_bullet(go_up)


    def set_bullet_position(self, go_up=False):
        """Set bullet position."""
        x, y = self.get_init_desired_bullet_pos(go_up)
        self.bullet.set_position(x, y)


    def process_bullet(self, go_up=False):
        """
        Decrease or increase the y position of bullet if it has benn fired.
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


    def render_explosions(self):
        """Render the ship when it is exploding."""
        # keep count in the indexes
        if self.count >= 11:
            self.count = 0

        # update time_before_shot until reach out the desired time
        if self.time_before_shot < self.time_after_shot:
            self.time_before_shot = time.time()

        # to avoid render sprites too fast, whait a few mili seconds
        if self.time_before_shot > self.time_after_shot:
            self.count += 1
            # update again, that way it does not blit many sprites at one moment
            self.time_after_shot = time.time() + 0.1
            self.update_time_after_shot = True

            # to avoid pop ship out too early
            if self.count == 11:
                self.pass_id = True

        # adjust the x position to the center of the ship
        rect = self.rect.copy()
        rect.x = self.rect.x + 12

        self.screen.blit(self.explosions_sprites[self.count], rect)


    def render(self):
        """
        Render image on screen. Also render bullet if it has been fired.
        """
        if self.destroyed:
            self.render_explosions()
        else:
            self.screen.blit(self.image, self.rect)

            if self.bullet.fired:
                self.bullet.render()



class Ship_Player(Ship):
    """Ship that the user will control."""

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

        # flag to know when stop game
        self.stop_game = False

        # time to close game after it's been destroyed
        self.time_to_close_game = time.time()
        self.time_to_wait = time.time()

        # stay at initial postion at the beginning
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False


    def check_keyup(self, event):
        """Check key up arrows events."""
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


    def process(self, fleet1, fleet2, close_game_function, go_up=True, ship_player=True):
        """Process ship and bullet."""
        self.keep_moving()

        # close game if player has been destroyed
        self.has_been_destroyed(close_game_function)

        super(self.__class__, self).process(go_up=go_up, fleet_1=fleet1, fleet_2=fleet2)


    def has_been_destroyed(self, close_game_function):
        """"If player has been destroyed close the game."""
        if self.destroyed:
            if self.time_to_wait > self.time_to_close_game:
                self.time_to_close_game = time.time() + 1.45
            else:
                self.time_to_wait = time.time()

            if self.time_to_wait > self.time_to_close_game:
                close_game_function()



class Ship_AI_Enemy(Ship):
    """Enemy ship with some AI."""

    def __init__(self, screen, bullet, x, y, id_ship=None):
        """Set position and turn image."""
        image_path = "images/ship.png"
        self.image = pygame.image.load(image_path).convert_alpha()

        # rotate image
        self.image = pygame.transform.rotate(self.image, 180)

        # get screen's rect
        screen_rect = screen.get_rect()

        speed = 1

        # store bullet
        self.bullet = bullet

        # rotate bullet
        self.bullet.image = pygame.transform.rotate(self.bullet.image, 180)

        # class superclass to initialize ship
        super(self.__class__, self).__init__(screen, self.image, self.bullet, speed, x, y, id_ship=id_ship)

        # set initial position of bullet
        self.set_bullet_position()

        # set default state machine. There are just two possible states: exploring and destroying
        self.state = "exploring"
        # flag to know whether or not it has reach out the destination
        self.has_come_dest = False

        # minimum distance to swtich to destroying state
        self.min_x_distance = 100
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
        min_x_distance = range(-self.min_x_distance, self.min_x_distance+10)

        if distance[0] in min_x_distance and distance[1] < self.min_y_distance:
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


    def process(self, ship, dead_ships):
        """Process all actions."""
        # set which one of the two state is appropiate
        self.can_see(ship)

        if self.state == "exploring":
            self.explore()
        else:
            self.destroy(ship)

        super(self.__class__, self).process(ship_player=ship)
        self.pass_id_to_dead_ships(dead_ships)
        self.collide_with(ship)


    def can_shoot_to(self, ship):
        """Shoot if it is in front of the ship."""
        # make a range of approximation of the x of ship
        range_x = range(ship.rect.x-2, ship.rect.x+2)
        if self.rect.x in range_x and self.rect.y < self.min_y_distance and \
        not self.rect.y >= ship.rect.y:
            return True
        else:
            return False


    def destroy(self, ship):
        """Try to destroy ship."""
        # if ship is in front, shoot it
        if self.can_shoot_to(ship) and not self.destroyed:
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


class Ship_Enemy(Ship):
    """Ship enemy."""

    def __init__(self, screen, bullet, x, y, id_ship=None):
        # load image
        image_path = "images/enemy.png"
        self.image = pygame.image.load(image_path).convert_alpha()

        self.speed = random.randint(1, 5)

        # initialize superclass
        super(self.__class__, self).__init__(screen, self.image, bullet, self.speed, x, y, id_ship=id_ship)

        # set initial bullet position
        self.set_bullet_position()

        # set destination
        self.dest_x = random.randint(self.screen_rect.left, self.screen_rect.right)
        self.dest_y = self.screen_rect.bottom + 50

        # times to decide when shoot
        self.time_to_shoot = time.time()
        self.time_to_wait = time.time() + 1


    def shoot(self):
        """Every seconds if the random number are right, shoot."""
        if self.time_to_shoot < self.time_to_wait:
            self.time_to_shoot = time.time()
        else:
            if random.randint(0, 50) == random.randint(0, 50):
                self.bullet.shoot()
                self.time_to_wait = time.time() + 1


    def process(self, ship, dead_ships):
        """Move to destination, and shoot randomly."""
        # shoot if a second has passed and the random numbers are right
        self.shoot()

        # move closer to destination
        self.move_x()
        self.move_y()

        # pass id to dead_ships if it is destroyed or out of screen
        self.pass_id_to_dead_ships(dead_ships)

        # others process, and see if it collide with ship
        super(self.__class__, self).process(ship_player=ship)
        super(self.__class__, self).collide_with(ship)


    def move_x(self):
        """Move closer to x destination."""
        if self.rect.x < self.dest_x:
            self.go_right()
        elif self.rect.x > self.dest_x:
            self.go_left()


    def move_y(self):
        """Move closer to y destination"""
        if not self.rect.y == self.dest_y:
            self.go_down()



class Fleet_Enemy:
    """"Fleet of Ships."""

    def __init__(self, screen, bullet_path, bullet_location, ai_ships=False):
        """Initialize fleet and set position."""
        # get screen's rect
        self.screen_rect = screen.get_rect()

        # id to identify ships in the dictionary
        self.id = 0
        # number of ships that will form the fleet
        if ai_ships:
            self.ships_number = 5
        else:
            self.ships_number = 0

        # will contain all ships and other one all id of
        # those that for one or another reason have to be deleted
        self.ships, self.dead_ships = {}, []

        # create ships
        self.make_ship(self.ships_number, screen, bullet_path, bullet_location, ai_ships)


    def make_ship(self, number_ships, screen, bullet_path, bullet_location, ai_ships=False):
        """Make n amount of ships and add it to the dict."""
        for x in range(number_ships):
            # instance a bullet for each ship
            bullet = Bullet(screen, bullet_path, bullet_location)

            # set position randomly
            x = random.randint(self.screen_rect.left, self.screen_rect.right)
            y = random.randint(self.screen_rect.top-200, self.screen_rect.bottom-500)

            # create ship with a random position
            if ai_ships:
                ship = Ship_AI_Enemy(screen, bullet, x, y, id_ship=self.id)
            else:
                ship = Ship_Enemy(screen, bullet, x, y, id_ship=self.id)
            ship.set_bullet_position()

            # add it to the dict
            self.ships[self.id] = ship
            # increase id to avoid use it again
            self.id += 1


    def render(self):
        """Render all the fleet."""
        for ship in self.ships.values():
            ship.render()


    def remove_ship(self):
        """Delete ship from the dictionary."""
        for id_ship in self.dead_ships:
            del self.ships[id_ship]
            self.dead_ships.remove(id_ship)


    def process(self, ship, ai_ships=False):
        """Process all actions of every ship."""
        for ship_e in self.ships.values():
            if ai_ships:
                ship_e.process(ship, self.dead_ships)
            else:
                ship_e.process(ship, self.dead_ships)

        # delete all those that are destroyed or out of screen
        self.remove_ship()
