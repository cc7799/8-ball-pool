import math
from math import pi, sin, cos
import unittest
import constants as c

# Cue Class #
import cue


class TestCue(unittest.TestCase):
    def setUp(self) -> None:
        self.center_of_rotation = (2, 2)
        self.rotation_offset = c.MIN_ROTATION_OFFSET
        self.cue_stick = cue.Cue(self.center_of_rotation)

    def test_distance_formula(self):
        self.assertEqual(self.cue_stick.distance_formula((1, 1), (4, 5)), 5)
        self.assertEqual(round(self.cue_stick.distance_formula((-1, -1), (4, 5)), 4), 7.8102)
        self.assertEqual(self.cue_stick.distance_formula((4, 5), (1, 1)), 5)

    def test_map_to_range(self):
        # Value middle of range; Input range larger than output
        self.assertEqual(self.cue_stick.map_to_range(5, (0, 10), (1, 5)), 3)
        # Value end of range; Input range smaller than output range
        self.assertEqual(self.cue_stick.map_to_range(5, (1, 5), (0, 10)), 10)
        # Input start of range
        self.assertEqual(self.cue_stick.map_to_range(1, (1, 5), (0, 10)), 0)

        # Both ranges start > 0
        self.assertEqual(self.cue_stick.map_to_range(2, (1, 9), (2, 6)), 2.5)

        # Checking returns for invalid input
        self.assertEqual(self.cue_stick.map_to_range(-1, (1, 5), (0, 10)), -1)  # input value negative
        self.assertEqual(self.cue_stick.map_to_range(1, (5, 2), (10, 1)),  -2)  # ranges must be in ascending order
        self.assertEqual(self.cue_stick.map_to_range(5, (1, 4), (1, 10)),  -3)  # input value larger or smaller than input range
        self.assertEqual(self.cue_stick.map_to_range(5, (1, 5), (-1, 10)), -4)  # ranges can't have negative values

    def test_split_velocity(self):
        answers = {"quad1": (-5 * sin(math.radians(45)), -5 * cos(math.radians(45))),
                   "quad2": (-5 * cos(math.radians(45)),  5 * sin(math.radians(45))),
                   "quad3": ( 5 * sin(math.radians(45)),  5 * cos(math.radians(45))),
                   "quad4": ( 5 * cos(math.radians(45)), -5 * sin(math.radians(45)))}

        # Quadrant 1
        self.assertEqual(self.cue_stick.split_velocity(5, 45),  answers["quad1"])
        # Quadrant 2
        self.assertEqual(self.cue_stick.split_velocity(5, 135), answers["quad2"])
        # Quadrant 3
        self.assertEqual(self.cue_stick.split_velocity(5, 225), answers["quad3"])
        # Quadrant 4
        self.assertEqual(self.cue_stick.split_velocity(5, 315), answers["quad4"])

        # The four cardinal directions
        self.assertEqual(self.cue_stick.split_velocity(5, 0),   ( 0, -5))
        self.assertEqual(self.cue_stick.split_velocity(5, 90),  (-5,  0))
        self.assertEqual(self.cue_stick.split_velocity(5, 180), ( 0,  5))
        self.assertEqual(self.cue_stick.split_velocity(5, 270), ( 5,  0))

        # Negative magnitude (should be equivalent to positive magnitude in opposite quadrant)
        self.assertEqual(self.cue_stick.split_velocity(-5, 45),  answers["quad3"])
        # Negative angle (should be equivalent to `angle % 360`)
        self.assertEqual(self.cue_stick.split_velocity(5, -45),  answers["quad4"])
        # Negative magnitude and angle (should be equivalent to pos. magnitude in opposite quadrant to `angle % 360`)
        self.assertEqual(self.cue_stick.split_velocity(-5, -45), answers["quad2"])

    def test_angle_to_point(self):
        answers = {"quad1": (self.center_of_rotation[0] + self.rotation_offset * math.sin(math.radians(45)),
                             self.center_of_rotation[1] + self.rotation_offset * math.cos(math.radians(45))),

                   "quad2": (self.center_of_rotation[0] + self.rotation_offset * math.cos(math.radians(45)),
                             self.center_of_rotation[1] - self.rotation_offset * math.sin(math.radians(45))),

                   "quad3": (self.center_of_rotation[0] - self.rotation_offset * math.sin(math.radians(45)),
                             self.center_of_rotation[1] - self.rotation_offset * math.cos(math.radians(45))),

                   "quad4": (self.center_of_rotation[0] - self.rotation_offset * math.cos(math.radians(45)),
                             self.center_of_rotation[1] + self.rotation_offset * math.sin(math.radians(45))),

                   "south": (self.center_of_rotation[0], self.center_of_rotation[1] + self.rotation_offset),

                   "east": (self.center_of_rotation[0] + self.rotation_offset, self.center_of_rotation[1]),

                   "north": (self.center_of_rotation[0], self.center_of_rotation[1] - self.rotation_offset),

                   "west": (self.center_of_rotation[0] - self.rotation_offset, self.center_of_rotation[1])}

        # Quadrant 1
        self.assertEqual(self.cue_stick.angle_to_point(45),  answers["quad1"])
        # Quadrant 2
        self.assertEqual(self.cue_stick.angle_to_point(135), answers["quad2"])
        # Quadrant 3
        self.assertEqual(self.cue_stick.angle_to_point(225), answers["quad3"])
        # Quadrant 4
        self.assertEqual(self.cue_stick.angle_to_point(315), answers["quad4"])

        # The four cardinal directions
        self.assertEqual(self.cue_stick.angle_to_point(0),   answers["south"])
        self.assertEqual(self.cue_stick.angle_to_point(90),  answers["east"])
        self.assertEqual(self.cue_stick.angle_to_point(180), answers["north"])
        self.assertEqual(self.cue_stick.angle_to_point(270), answers["west"])

        # Negative angle (should be equivalent to `angle % 360`)
        self.assertEqual(self.cue_stick.angle_to_point(-45), answers["quad4"])

    def test_point_to_angle(self):
        points = {"quad1": (self.center_of_rotation[0] + 2, self.center_of_rotation[1] + 1),
                  "quad2": (self.center_of_rotation[0] + 2, self.center_of_rotation[1] - 1),
                  "quad3": (self.center_of_rotation[0] - 2, self.center_of_rotation[1] - 1),
                  "quad4": (self.center_of_rotation[0] - 2, self.center_of_rotation[1] + 1)}

        # Center of rotation is (2, 2)

        # Quadrant tests will always have a delta_x of 2 and a delta_y of 1
        # Quadrant 1
        self.assertEqual(self.cue_stick.point_to_angle((4, 3)), math.degrees(math.atan(2 / 1)))
        # Quadrant 2
        self.assertEqual(self.cue_stick.point_to_angle((4, 1)), math.degrees(math.atan(1 / 2)) + 90)
        # Quadrant 3
        self.assertEqual(self.cue_stick.point_to_angle((0, 1)), math.degrees(math.atan(2 / 1)) + 180)
        # Quadrant 4
        self.assertEqual(self.cue_stick.point_to_angle((0, 3)), math.degrees(math.atan(1 / 2)) + 270)

        # Cardinals
        # South (delta_x = 0, delta_y = 2)
        self.assertEqual(self.cue_stick.point_to_angle((2, 4)), 0)
        # East (delta_x = 2, delta_y = 0)
        self.assertEqual(self.cue_stick.point_to_angle((4, 2)), 90)
        # North (delta_x = 0, delta_y = 2)
        self.assertEqual(self.cue_stick.point_to_angle((2, 0)), 180)
        # East (delta_x = 2, delta_y = 0)
        self.assertEqual(self.cue_stick.point_to_angle((0, 2)), 270)

        # Same point as center of rotation
        self.assertEqual(self.cue_stick.point_to_angle((2, 2)), 0)

    def test_check_valid_set_power_mouse_pos(self):
        # Cue stick is currently at angle 0 with center of rotation (2, 2)

        # Mouse at point of rotation
        self.assertEqual(self.cue_stick.check_valid_power_mouse_pos((2, 2)), True)

        # Mouse at same angle as cue
        self.assertEqual(self.cue_stick.check_valid_power_mouse_pos((2, 4)), True)

        # Mouse at +45 degrees
        self.assertEqual(self.cue_stick.check_valid_power_mouse_pos((3, 3)), True)

        # Mouse at -45 degrees
        self.assertEqual(self.cue_stick.check_valid_power_mouse_pos((1, 3)), True)

        # Mouse at 90 degrees
        self.assertEqual(self.cue_stick.check_valid_power_mouse_pos((3, 2)), False)

    def test_set_cue_power(self):
        pass

    def test_set_rotation_point(self):
        # Positive point
        self.cue_stick.set_rotation_point((3, 5))
        self.assertEqual(self.cue_stick.rotation_point, (3, 5))

        # Negative point
        self.cue_stick.set_rotation_point((-2, -3))
        self.assertEqual(self.cue_stick.rotation_point, (-2, -3))

        # Reset point
        self.cue_stick.set_rotation_point((2, 2))

    def test_reset_offset(self):
        self.cue_stick.rotation_offset = 200
        self.cue_stick.reset_rotation()

        self.assertEqual(self.cue_stick.rotation_offset, c.MIN_ROTATION_OFFSET)


if __name__ == "__main__":
    unittest.main()
