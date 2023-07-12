import math
from typing import Dict, Tuple

import numpy as np
import pygame

import constants as c
from constants import BallTypes, Point
import utilities as util


COLORLIST = [c.colors["white"], c.colors["yellow"], c.colors["blue"], c.colors["red"], c.colors["purple"],
             c.colors["orange"], c.colors["green"], c.colors["maroon"], c.colors["black"]]


class PoolBall(pygame.sprite.Sprite):
    def __init__(self, num: int, position: Point):
        super().__init__()

        self.image = pygame.Surface([2 * c.BALL_RADIUS, 2 * c.BALL_RADIUS], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        self.x_pos = self.rect.x = position.x
        self.y_pos = self.rect.y = position.y
        self.x_velo = self.y_velo = 0

        self.num = num
        self.in_play = True

        if num == 8:
            self.color = COLORLIST[8]
        else:
            self.color = COLORLIST[num % 8]

        # Flags #
        self.visible = True
        self.moving = False

        self.type: BallTypes
        if num == 0:
            self.type = BallTypes.cue
        elif num < 8:
            self.type = BallTypes.solid
        elif num == 8:
            self.type = BallTypes.eight
        else:
            self.type = BallTypes.striped

        self.create_image()

    def __eq__(self, other) -> bool:
        """
        Checks if the numbers of the balls are the same
        :param other: The other ball to check
        :return: True if other is a PoolBall and has the same number as self; False otherwise
        """
        if type(other) != type(self):
            return False

        return self.num == other.num

    def __hash__(self):
        """
        Hashes the ball based on its number
        """
        return hash(self.num)

    def create_image(self) -> None:
        """
        Creates the ball's image based on its type
        """
        if self.in_play:
            if self.type == BallTypes.striped:
                pygame.draw.circle(self.image, c.colors["white"], [c.BALL_RADIUS, c.BALL_RADIUS], c.BALL_RADIUS)
                pygame.draw.rect(self.image, self.color, pygame.Rect(1, c.BALL_RADIUS - c.BALL_RADIUS / 2, 2 * c.BALL_RADIUS - 2, c.BALL_RADIUS))

            else:
                pygame.draw.circle(self.image, self.color, (c.BALL_RADIUS, c.BALL_RADIUS), c.BALL_RADIUS)

            pygame.draw.circle(self.image, c.colors["white"], (c.BALL_RADIUS, c.BALL_RADIUS), c.BALL_RADIUS / 2)

    def move(self):
        """
        Moves the ball based on its current velocity
        """
        # Collision with top wall
        if self.rect.y < 30 + c.SCREEN_HEIGHT_PADDING:
            self.y_velo = -self.y_velo * c.BOUNCE_MODIFIER
            self.rect.y = 31 + c.SCREEN_HEIGHT_PADDING
            self.y_pos = self.rect.y

        # Collision with bottom wall
        elif self.rect.y > c.POOL_TABLE_HEIGHT - 31 - (c.BALL_RADIUS * 2) + c.SCREEN_HEIGHT_PADDING:
            self.y_velo = -self.y_velo * c.BOUNCE_MODIFIER
            self.rect.y = c.POOL_TABLE_HEIGHT - 31 - (c.BALL_RADIUS * 2) + c.SCREEN_HEIGHT_PADDING
            self.y_pos = self.rect.y

        # Collision with right wall
        elif self.rect.x > c.POOL_TABLE_WIDTH - 31 - (c.BALL_RADIUS * 2) + c.SCREEN_WIDTH_PADDING:
            self.x_velo = -self.x_velo * c.BOUNCE_MODIFIER
            self.rect.x = c.POOL_TABLE_WIDTH - 31 - (c.BALL_RADIUS * 2) + c.SCREEN_WIDTH_PADDING
            self.x_pos = self.rect.x

        # Collision left wall
        elif self.rect.x < 30 + c.SCREEN_WIDTH_PADDING:
            self.x_velo = -self.x_velo * c.BOUNCE_MODIFIER
            self.rect.x = 31 + c.SCREEN_WIDTH_PADDING
            self.x_pos = self.rect.x

        self.set_position(Point(self.x_pos + self.x_velo, self.y_pos + self.y_velo))

        if self.x_velo != 0 or self.y_velo != 0:
            x_ratio = math.fabs(self.x_velo) / (math.fabs(self.x_velo) + math.fabs(self.y_velo))
            if self.x_velo < -c.FRICTION:
                self.x_velo += x_ratio * c.FRICTION
            elif self.x_velo > c.FRICTION:
                self.x_velo -= x_ratio * c.FRICTION
            else:
                self.x_velo = 0

            if self.y_velo < - c.FRICTION:
                self.y_velo += (1 - x_ratio) * c.FRICTION
            elif self.y_velo > c.FRICTION:
                self.y_velo -= (1 - x_ratio) * c.FRICTION
            else:
                self.y_velo = 0

    def has_collided_with(self, ball2) -> bool:
        """
        Determines if the current ball has collided with the given ball
        :param ball2: The ball to check for collision with
        :return: True if the balls have collided; False otherwise
        """
        x_distance = self.rect.x - ball2.rect.x
        y_distance = self.rect.y - ball2.rect.y
        side_1 = math.sqrt(x_distance * x_distance + y_distance * y_distance)
        return side_1 < 2 * c.BALL_RADIUS

    def apply_scale_value(self, scale_val: float) -> None:
        """
        Applies a scale value to the position of the ball. Used to help prevent clipping
        :param scale_val: The value to change the position by
        """
        if scale_val < 1:
            scale_val = 1

        new_x = new_y = 0

        if self.x_velo < 0:
            new_x = self.x_pos + scale_val
        elif self.x_velo >= 0:
            new_x = self.x_pos - scale_val

        if self.y_velo < 0:
            new_y = self.y_pos + scale_val
        elif self.y_velo >= 0:
            new_y = self.y_pos - scale_val

        self.set_position(Point(new_x, new_y))

    def collision(self, ball2) -> None:
        """
        Controls the collision between two pool balls
        :param ball2: The ball that the current ball is colliding with
        """
        def calculate_and_set_new_velocities() -> None:
            """
            Calculates the new velocities after the collision and sets them as the balls' velocities
            """
            collision_strength: np.array = position_change / distance

            # Use the dot product to calculate new velocities
            ball1_velocity = np.array([self.x_velo, self.y_velo], dtype=float)
            ball2_velocity = np.array([ball2.x_velo, ball2.y_velo], dtype=float)

            ball1_dot = np.dot(ball1_velocity, collision_strength)
            ball2_dot = np.dot(ball2_velocity, collision_strength)

            # since the masses of the balls are the same, the velocity will just switch
            ball1_velocity = (ball2_dot - ball1_dot) * collision_strength * 0.5 * (1 + c.BOUNCE_MODIFIER)
            ball2_velocity = (ball1_dot - ball2_dot) * collision_strength * 0.5 * (1 + c.BOUNCE_MODIFIER)

            self.set_velocity(ball1_velocity)
            ball2.set_velocity(ball2_velocity)

        def prevent_and_correct_clipping() -> None:
            """
            Helps to prevent clipping and correct it when it occurs
            """
            # Move the balls a little to prevent clipping. This works pretty well I have found.
            scale_value = (np.sqrt(self.x_velo ** 2 + self.y_velo ** 2)) / 2
            self.apply_scale_value(scale_value)
            ball2.apply_scale_value(scale_value)

            # if this is true they are almost certainly clipping and badly
            if distance <= 1 * c.BALL_RADIUS:
                if c.DEBUGGING:
                    print("[DEBUG-pool_ball.py]: clip detected with distance between balls of " + str(distance))
                self.set_position(Point(20 - distance, 20 - distance))
                ball2.set_position(Point(20 - distance, 20 - distance))

        # Geta the coordinates of balls for dot product
        ball1_pos_array:  np.array = np.array([self.rect.x, self.rect.y], dtype=np.single)
        ball2_pos_array:  np.array = np.array([ball2.rect.x, ball2.rect.y], dtype=np.single)
        position_change: np.array = ball1_pos_array - ball2_pos_array

        # distance: float = util.distance_formula(self.get_position(), ball2.get_position())

        distance = util.distance_formula(self.get_position(), ball2.get_position())

        # If this is true they have touched
        if distance <= 2 * c.BALL_RADIUS:
            prevent_and_correct_clipping()

            calculate_and_set_new_velocities()

        # Update the positions of the balls
        self.set_position(Point(self.x_pos + self.x_velo, self.y_pos + self.y_velo))

        ball2.set_position(Point(ball2.x_pos + ball2.x_velo, ball2.y_pos + ball2.y_velo))

    def in_pocket(self) -> bool:
        """
        Determines if a ball is in a pocket
        :return: True if the ball is in a pocket; False otherwise
        """
        if (((self.rect.x < 35 + c.SCREEN_WIDTH_PADDING)
             and (self.rect.y < 35 + c.SCREEN_HEIGHT_PADDING)) or
                ((self.rect.x < 35 + c.SCREEN_WIDTH_PADDING)
                 and (self.rect.y > 345 + c.SCREEN_HEIGHT_PADDING)) or
                ((self.rect.x > 745 + c.SCREEN_WIDTH_PADDING)
                 and (self.rect.y < 35 + c.SCREEN_HEIGHT_PADDING)) or
                ((self.rect.x > 745 + c.SCREEN_WIDTH_PADDING)
                 and (self.rect.y > 345 + c.SCREEN_HEIGHT_PADDING)) or
                ((self.rect.x in range(375 + c.SCREEN_WIDTH_PADDING, 410 + c.SCREEN_WIDTH_PADDING))
                 and (self.rect.y < 35 + c.SCREEN_HEIGHT_PADDING)) or
                ((self.rect.x in range(375 + c.SCREEN_WIDTH_PADDING, 410 + c.SCREEN_WIDTH_PADDING))
                 and (self.rect.y > 345 + c.SCREEN_HEIGHT_PADDING))):
            return True
        else:
            return False

    def display_ball_below(self, num_balls_in: Dict[BallTypes, int]) -> None:
        """
        Displays the ball in the scorecard area of the board
        :param num_balls_in: A dictionary containing the number of balls in for the types solid and striped
        """
        self.in_play = False

        self.set_velocity((0, 0))

        self.set_position(Point(self.x_pos, 440 + c.SCREEN_WIDTH_PADDING))

        if self.type == BallTypes.striped:
            self.set_position(Point(55 * num_balls_in[BallTypes.striped] + 28 + c.SCREEN_WIDTH_PADDING, self.y_pos))
        else:
            self.set_position(Point(55 * num_balls_in[BallTypes.solid] + 28 + 395 + c.SCREEN_WIDTH_PADDING, self.y_pos))

    def set_position(self, position: Point) -> None:
        """
        Sets the position of the pool ball
        :param position: A tuple containing the x- and y-coordinates of the top-left corner of the ball
        """
        self.x_pos = self.rect.x = position.x

        self.y_pos = self.rect.y = position.y

    def set_x_position(self, x: float) -> None:
        """
        Sets the x-coordinate of the top-left corner of the ball
        :param x: The x-coordinate to set
        """
        self.set_position(Point(x, self.y_pos))

    def set_y_position(self, y: float) -> None:
        """
        Sets the y-coordinate of the top-left corner of the ball
        :param y: The y-coordinate to set
        """
        self.set_position(Point(self.x_pos, y))

    def set_velocity(self, velocity: Tuple[float, float]) -> None:
        """
        Sets the velocity of the ball
        :param velocity: A tuple containing the x- and y-portions of the velocity
        """
        # Round the velocity because we have had problems with it if it gets too small
        self.x_velo = round(velocity[0], 5)
        self.y_velo = round(velocity[1], 5)

    def get_position(self) -> Point:
        """
        Gets the position of the ball
        :return: A tuple containing the x- and y-coordinates of the top-left corner of the ball
        """
        return Point(self.x_pos, self.y_pos)

    def is_moving(self) -> bool:
        """
        Determines if the ball is moving
        :return: True if the ball has any velocity; False otherwise
        """
        if (math.fabs(self.x_velo) <= 0) and (math.fabs(self.y_velo) <= 0):
            return False
        else:
            return True
