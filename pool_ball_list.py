import itertools
from typing import List, Tuple

import pygame.sprite

from constants import Point
from pool_ball import PoolBall


class PoolBallList:
    def __init__(self):
        """
        Creates a list to store the pool balls and a sprite group to allow updating and drawing the pool balls
        """
        # List filled with 16 invalid balls, will be filled later
        self.pool_balls: List[PoolBall] = [PoolBall(-1, Point(0, 0))] * 16

        self.sprite_group: pygame.sprite.Group = pygame.sprite.Group()

    def add_ball(self, ball_number: int, stating_position: Point) -> None:
        """
        Adds a ball to the list
        :param ball_number: The number of the ball; 0 is used for the cue ball
        :param stating_position: The x- and y-coordinates of the starting position of the ball
        """
        new_ball = PoolBall(ball_number, stating_position)

        self.pool_balls[ball_number] = new_ball

        self.sprite_group.add(new_ball)

    def get(self, ball_num: int) -> PoolBall:
        """
        Returns the pool ball with the given number
        :param ball_num: The number of the ball to get
        :return: The PoolBall object with number `ball_num`
        """
        return self.pool_balls[ball_num]

    def move_balls(self) -> Tuple[PoolBall, ]:
        """
        Move all the balls based on their velocity
        :return: A tuple containing any balls that went into a pocket
        """
        # A list of the balls that went into a pocket during this set of movement
        balls_in_pocket: List[PoolBall] = []

        for ball in self.pool_balls:
            if ball.in_play:
                ball.move()

                if ball.in_pocket():
                    balls_in_pocket.append(ball)
                    ball.in_play = False

        return tuple(balls_in_pocket)

    def perform_collisions(self):
        """
        Perform the collisions on all the balls
        :return: True if any balls collided; False otherwise
        """
        any_ball_collided = False

        for ball_pair in itertools.combinations(self.pool_balls, 2):
            if ball_pair[0].has_collided_with(ball_pair[1]):
                ball_pair[0].collision(ball_pair[1])
                any_ball_collided = True

        return any_ball_collided

    def all_balls_stationary(self) -> bool:
        """
        Determines if all the balls are stationary
        :return: True if all the balls are stationary; False otherwise
        """
        for ball in self.pool_balls:
            if ball.is_moving():
                return False

        return True

    def draw(self, display_surface: pygame.surface) -> None:
        """
        Draws every ball sprite
        :param display_surface: The surface to draw the ball's onto
        """
        draw_group = pygame.sprite.Group()
        for ball in self.pool_balls:
            if ball.visible:
                draw_group.add(ball)

        draw_group.draw(display_surface)

    def hide_ball(self, ball_num: int) -> False:
        """
        Hides a given ball
        :param ball_num: The number of the ball to hide
        """
        self.pool_balls[ball_num].visible = False

    def show_ball(self, ball_num: int) -> None:
        """
        Shows a given ball
        :param ball_num: The number of the ball to show
        """
        self.pool_balls[ball_num].visible = True

    def hide_all_balls(self) -> None:
        """
        Hides every ball
        """
        for ball in self.pool_balls:
            ball.visible = False

    def show_all_balls(self) -> None:
        """
        Shows every ball
        """
        for ball in self.pool_balls:
            ball.visible = True

    def get_num_balls(self):
        """
        Returns the total number of balls
        :return: The length of the ball list
        """
        return len(self.pool_balls)
