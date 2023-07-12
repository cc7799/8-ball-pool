import math
import pygame
from typing import Tuple

import constants as c
from constants import Point


def distance_formula(point1: Point, point2: Point) -> float:
    """
    Calculates the distance between two points on a 2D plane
    :param point1: The first point
    :param point2: The second point
    :return: The distance between the two points
    """
    part1 = (point2.x - point1.x) ** 2
    part2 = (point2.y - point1.y) ** 2

    distance = math.sqrt((part1 + part2))

    return distance


def map_to_range(input_value: float, input_range: Tuple[float, float], output_range: Tuple[float, float]) -> float:
    """
    Maps a given  value in a given range to the equivalent value in a second range
    For example, mapping 5 and 10 in the range 0-10 onto the range 1-5 would output 3 and 5
    Uses the formula `output = output_range_length * ([input - input_range[0]] / input_range_length)`
    :param input_value: The value to map. Must be positive
    :param input_range: The range to map from. Must be positive and the first value must be smaller than the second
    :param output_range: The range to map to. Must be positive and the first value must be smaller than the second
    :return: The equivalent of the input in the output range if the input value is positive
                and within the input range; returns negative number otherwise
    """
    # Check for valid inputs
    if input_value < 0:
        return -1
    if input_range[1] < input_range[0] or output_range[1] < output_range[0]:
        return -2
    if input_value < input_range[0] or input_value > input_range[1]:
        return -3
    if input_range[0] < 0 or input_range[1] < 0 or output_range[0] < 0 or output_range[1] < 0:
        return -4

    input_range_len = input_range[1] - input_range[0]
    output_range_len = output_range[1] - output_range[0]

    # Since the percentage is based on the length instead of the max of the range,
    #   the input value must be lowered by the difference between the max value and the length,
    #   which will always be the min value of the range.
    adjusted_input_value = input_value - input_range[0]
    # What percent of the range length is before the input
    input_percentage = adjusted_input_value / input_range_len

    output_value = output_range[0] + (output_range_len * input_percentage)

    return output_value


def get_text_start_position(font: pygame.font.Font, text: str, center_vertically: bool = None) -> Point:
    """
    Gets the start position of a given string in a given font to center it at the top of the screen
    :param font: The font object to use
    :param text: The text to position
    :param center_vertically: Whether the text should be center along the y-axis as well
    :return: A Point containing the x- and y-coordinates of the start position of the text
    """
    width, height = font.size(text)

    x_pos = (c.SCREEN_WIDTH / 2) - (width / 2)
    y_pos = (c.SCREEN_HEIGHT / 2) - (height / 2)

    if center_vertically:
        return Point(x_pos, y_pos)
    else:
        return Point(x_pos, 0)


def get_text_start_position_two_lines(font: pygame.font.Font, line1: str, line2: str) -> Tuple[Point, Point]:
    """
    Gets the start positions of two strings in a given font to center them in the center of the screen
        with spacing between them
    :param font: The font object to use
    :param line1: The text on top
    :param line2: The text on bottom
    :return: A tuple containing Points of the x- and y-coordinates of the two line
    """
    width1, height1 = font.size(line1)
    width2, height2 = font.size(line2)

    x1 = (c.SCREEN_WIDTH / 2) - (width1 / 2)
    x2 = (c.SCREEN_WIDTH / 2) - (width2 / 2)

    y1 = (c.SCREEN_HEIGHT / 2) - (height1 / 2) - height2
    y2 = (c.SCREEN_HEIGHT / 2) - (height2 / 2) + height1

    return Point(x1, y1), Point(x2, y2)

