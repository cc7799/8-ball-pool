import math
from math import pi, sin, cos
import unittest
import constants as c
from constants import Point
import utilities as util
import pygame

# Cue Class #
import cue


class TestCue(unittest.TestCase):
    def setUp(self) -> None:
        self.center_of_rotation = Point(2, 2)
        self.rotation_offset = c.MIN_ROTATION_OFFSET
        self.cue_stick = cue.Cue(self.center_of_rotation)

    # Test `utilities.py` #
    def test_distance_formula(self):
        self.assertEqual(util.distance_formula(Point(1, 1), Point(4, 5)), 5)
        self.assertEqual(round(util.distance_formula(Point(-1, -1), Point(4, 5)), 4), 7.8102)
        self.assertEqual(util.distance_formula(Point(4, 5), Point(1, 1)), 5)

    def test_map_to_range(self):
        # Value middle of range; Input range larger than output
        self.assertEqual(util.map_to_range(5, (0, 10), (1, 5)), 3)
        # Value end of range; Input range smaller than output range
        self.assertEqual(util.map_to_range(5, (1, 5), (0, 10)), 10)
        # Input start of range
        self.assertEqual(util.map_to_range(1, (1, 5), (0, 10)), 0)

        # Both ranges start > 0
        self.assertEqual(util.map_to_range(2, (1, 9), (2, 6)), 2.5)

        # Checking returns for invalid input
        self.assertEqual(util.map_to_range(-1, (1, 5), (0, 10)), -1)  # input value negative
        self.assertEqual(util.map_to_range(1, (5, 2), (10, 1)), -2)  # ranges must be in ascending order
        self.assertEqual(util.map_to_range(5, (1, 4), (1, 10)), -3)  # input value larger or smaller than input range
        self.assertEqual(util.map_to_range(5, (1, 5), (-1, 10)), -4)  # ranges can't have negative values

    # Test `cue.py` #
    def test_rotate(self):
        self.cue_stick.rotate(0)
        self.assertEqual(self.cue_stick.angle, 0)

        self.cue_stick.rotate(45)
        self.assertEqual(self.cue_stick.angle, 45)

        self.cue_stick.rotate(450)
        self.assertEqual(self.cue_stick.angle, 90)

        self.cue_stick.rotate(-45)
        self.assertEqual(self.cue_stick.angle, 315)

        self.cue_stick.rotate(0)  # Reset rotation

    def test_angle_to_point(self):
        answers = {"quad1": Point(self.center_of_rotation.x + self.rotation_offset * math.sin(math.radians(45)),
                                  self.center_of_rotation.y + self.rotation_offset * math.cos(math.radians(45))),

                   "quad2": Point(self.center_of_rotation.x + self.rotation_offset * math.cos(math.radians(45)),
                                  self.center_of_rotation.y - self.rotation_offset * math.sin(math.radians(45))),

                   "quad3": Point(self.center_of_rotation.x - self.rotation_offset * math.sin(math.radians(45)),
                                  self.center_of_rotation.y - self.rotation_offset * math.cos(math.radians(45))),

                   "quad4": Point(self.center_of_rotation.x - self.rotation_offset * math.cos(math.radians(45)),
                                  self.center_of_rotation.y + self.rotation_offset * math.sin(math.radians(45))),

                   "south": Point(self.center_of_rotation.x, self.center_of_rotation.y + self.rotation_offset),

                   "east": Point(self.center_of_rotation.x + self.rotation_offset, self.center_of_rotation.y),

                   "north": Point(self.center_of_rotation.x, self.center_of_rotation.y - self.rotation_offset),

                   "west": Point(self.center_of_rotation.x - self.rotation_offset, self.center_of_rotation.y)}

        # Quadrant 1
        self.assertEqual(self.cue_stick.angle_to_point(45), answers["quad1"])
        # Quadrant 2
        self.assertEqual(self.cue_stick.angle_to_point(135), answers["quad2"])
        # Quadrant 3
        self.assertEqual(self.cue_stick.angle_to_point(225), answers["quad3"])
        # Quadrant 4
        self.assertEqual(self.cue_stick.angle_to_point(315), answers["quad4"])

        # The four cardinal directions
        self.assertEqual(self.cue_stick.angle_to_point(0), answers["south"])
        self.assertEqual(self.cue_stick.angle_to_point(90), answers["east"])
        self.assertEqual(self.cue_stick.angle_to_point(180), answers["north"])
        self.assertEqual(self.cue_stick.angle_to_point(270), answers["west"])

        # Negative angle (should be equivalent to `angle % 360`)
        self.assertEqual(self.cue_stick.angle_to_point(-45), answers["quad4"])

    def test_point_to_angle(self):
        # Center of rotation is (2, 2)

        # Quadrant tests will always have a delta_x of 2 and a delta_y of 1
        # Quadrant 1
        self.assertEqual(self.cue_stick.point_to_angle(Point(4, 3)), math.degrees(math.atan(2 / 1)))
        # Quadrant 2
        self.assertEqual(self.cue_stick.point_to_angle(Point(4, 1)), math.degrees(math.atan(1 / 2)) + 90)
        # Quadrant 3
        self.assertEqual(self.cue_stick.point_to_angle(Point(0, 1)), math.degrees(math.atan(2 / 1)) + 180)
        # Quadrant 4
        self.assertEqual(self.cue_stick.point_to_angle(Point(0, 3)), math.degrees(math.atan(1 / 2)) + 270)

        # Cardinals
        # South (delta_x = 0, delta_y = 2)
        self.assertEqual(self.cue_stick.point_to_angle(Point(2, 4)), 0)
        # East (delta_x = 2, delta_y = 0)
        self.assertEqual(self.cue_stick.point_to_angle(Point(4, 2)), 90)
        # North (delta_x = 0, delta_y = 2)
        self.assertEqual(self.cue_stick.point_to_angle(Point(2, 0)), 180)
        # East (delta_x = 2, delta_y = 0)
        self.assertEqual(self.cue_stick.point_to_angle(Point(0, 2)), 270)

        # Same point as center of rotation
        self.assertEqual(self.cue_stick.point_to_angle(Point(2, 2)), 0)

    # TODO: Add checks for if the cue power is being set properly
    def test_set_cue_power(self):
        # Cue stick is currently at angle 0 with center of rotation (2, 2)

        # Mouse at point of rotation
        self.assertEqual(self.cue_stick.set_cue_power(Point(2, 2)), True)

        # Mouse at same angle as cue
        self.assertEqual(self.cue_stick.set_cue_power(Point(2, 4)), True)

        # Mouse at +45 degrees
        self.assertEqual(self.cue_stick.set_cue_power(Point(3, 3)), True)

        # Mouse at -45 degrees
        self.assertEqual(self.cue_stick.set_cue_power(Point(1, 3)), True)

        # Mouse at 90 degrees
        self.assertEqual(self.cue_stick.set_cue_power(Point(3, 2)), False)

    # TODO: Complete
    def test_set_cue_power_to_offset(self):
        pass

    def test_reset_rotation(self):
        self.cue_stick.rotation_offset = 200
        self.cue_stick.reset_rotation()

        self.assertEqual(self.cue_stick.rotation_offset, c.MIN_ROTATION_OFFSET)

    def test_determine_cue_velocity(self):
        answers = {"quad1": (-5 * sin(math.radians(45)), -5 * cos(math.radians(45))),
                   "quad2": (-5 * cos(math.radians(45)), 5 * sin(math.radians(45))),
                   "quad3": (5 * sin(math.radians(45)), 5 * cos(math.radians(45))),
                   "quad4": (5 * cos(math.radians(45)), -5 * sin(math.radians(45)))}

        self.cue_stick.rotation_offset = c.MAX_ROTATION_OFFSET
        # Quadrant 1
        self.cue_stick.rotate(45)
        self.assertEqual(self.cue_stick.determine_cue_ball_velocity(), answers["quad1"])
        # Quadrant 2
        self.cue_stick.rotate(135)
        self.assertEqual(self.cue_stick.determine_cue_ball_velocity(), answers["quad2"])
        # Quadrant 3
        self.cue_stick.rotate(225)
        self.assertEqual(self.cue_stick.determine_cue_ball_velocity(), answers["quad3"])
        # Quadrant 4
        self.cue_stick.rotate(315)
        self.assertEqual(self.cue_stick.determine_cue_ball_velocity(), answers["quad4"])

        # The four cardinal directions
        self.cue_stick.rotate(0)
        self.assertEqual(self.cue_stick.determine_cue_ball_velocity(), (0, -5))

        self.cue_stick.rotate(90)
        self.assertEqual(self.cue_stick.determine_cue_ball_velocity(), (-5, 0))

        self.cue_stick.rotate(180)
        self.assertEqual(self.cue_stick.determine_cue_ball_velocity(), (0, 5))

        self.cue_stick.rotate(270)
        self.assertEqual(self.cue_stick.determine_cue_ball_velocity(), (5, 0))


if __name__ == "__main__":
    unittest.main()
