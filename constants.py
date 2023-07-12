from dataclasses import dataclass, astuple
from enum import Enum
from typing import Dict, Tuple, List

import pygame


# Enums #
class Players(Enum):
    """
    The two players
    """
    player1 = 0
    player2 = 1

    def __str__(self):
        if self.value == 0:
            return "Player 1"
        elif self.value == 1:
            return "Player 2"

    def swap_player(self):
        """
        Swaps the current player type
        :return: The opposite Players object to the current one
        """
        swapped_value = (self.value + 1) % 2

        return Players(swapped_value)


class GamePhases(Enum):
    """
    The five phases of the game
    """
    place_cue = 0
    hit_cue = 1
    ball_in_play = 2
    game_over = 3
    quit = 4


class BallTypes(Enum):
    """
    The four types of balls
    """
    cue = 0
    eight = 1
    striped = 2
    solid = 3

    def swap_type(self):
        """
        Swaps between solid and striped balls. Keeps cue and eight balls the same.
        :return: The proper BallType
        """
        if self.value == 0 or self.value == 1:
            return BallTypes(self.value)
        elif self.value == 2:
            return self.solid
        elif self.value == 3:
            return self.striped


@dataclass
class Point:
    x: float
    y: float

    def to_tuple(self) -> Tuple:
        return astuple(self)

    @staticmethod
    def get_point(tuple_point: Tuple[float, float]):
        return Point(tuple_point[0], tuple_point[1])


# Data Constants #
colors: Dict[str, Tuple[int, int, int]] = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255),
    "maroon": (119, 7, 55),
    "orange": (255, 172, 28),
    "purple": (128, 0, 128),
    "yellow": (255, 234, 0),

    "pool_silver": (192, 192, 192),
    "pool_black": (0, 0, 0),
    "pool_brown": (102, 51, 0),
    "pool_green": (20, 120, 20),

    "deep_pink": (255, 20, 147)
}


# Operation Constants #
DEBUGGING = True
MAX_FRAMERATE = 60

DIGIT_EVENTS: List[pygame.event] = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                    pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
                                    pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t,
                                    pygame.K_y, pygame.K_u]

# Physics Constants #
FRICTION = 1 / 128
BOUNCE_MODIFIER = .95

# Screen & Background Constants #
SCREEN_WIDTH_PADDING = 125
SCREEN_HEIGHT_PADDING = 125

SCREEN_WIDTH = 800 + (2 * SCREEN_WIDTH_PADDING)
SCREEN_HEIGHT = 400 + (2 * SCREEN_WIDTH_PADDING) + 100

POOL_TABLE_WIDTH = 800
POOL_TABLE_HEIGHT = 400

TABLE_HEAD_STRING_LOCATION = (30 + SCREEN_WIDTH_PADDING) + ((POOL_TABLE_WIDTH - 60) * 0.75)

POCKET_LOCATIONS = [[35, 35], [35, 345], [745, 35], [745, 345], [392, 35], [392, 345]]

# Ball Constants #
BALL_RADIUS = 10

# TODO: make locations dependent on screen size
CUE_BALL_START_LOCATION = Point(0, 0)
EIGHT_BALL_START_LOCATION = Point(160 + SCREEN_WIDTH_PADDING, 190 + SCREEN_HEIGHT_PADDING)

REGULAR_POOL_BALL_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]
REGULAR_POOL_BALL_START_LOCATIONS: List[Point] = [Point(200, 190), Point(180, 203), Point(180, 177), Point(160, 214),
                                                  Point(160, 166), Point(140, 226), Point(140, 203), Point(140, 177),
                                                  Point(140, 154), Point(119, 237), Point(119, 214), Point(119, 190),
                                                  Point(119, 166), Point(119, 143)]


# TODO: Remove after solving previous TODO
# Accounts for the screen padding in the positions
temp_starts = []
for pb in REGULAR_POOL_BALL_START_LOCATIONS:
    temp_starts.append(Point(pb.x + SCREEN_WIDTH_PADDING, pb.y + SCREEN_HEIGHT_PADDING))
REGULAR_POOL_BALL_START_LOCATIONS = temp_starts

# Cue constants #
CUE_WIDTH = 15
CUE_HEIGHT = 250
HALF_CUE_HEIGHT = CUE_HEIGHT / 2

EDGE_OF_BALL_OFFSET = HALF_CUE_HEIGHT + BALL_RADIUS

MIN_ROTATION_OFFSET = EDGE_OF_BALL_OFFSET + 5
MAX_ROTATION_OFFSET = MIN_ROTATION_OFFSET + 100

MAX_CUE_BALL_VELO = 5  # The speed the cue ball should go at if hit at max draw distance

# Text Constants #
PLAYER_TEXT_FONT_FILENAME = "fonts/Arcade.ttf"
PLAYER_TEXT_FONT_SIZE = 100
PLAYER_TEXT_COLOR = colors["blue"]
WINNER_TEXT_FONT_FILENAME = "fonts/abduction2002.ttf"
WINNER_TEXT_FONT_SIZE = 200
WINNER_TEXT_COLOR = colors["deep_pink"]
