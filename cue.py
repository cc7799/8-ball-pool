import pygame
import math
import constants as c
from typing import Tuple
import utilities as util
from constants import Point


class Cue(pygame.sprite.Sprite):
    def __init__(self, center_of_rotation: Point):
        super().__init__()

        # The point that the cue rotates around. Should always be the center of the cue ball
        self.rotation_point: Point = center_of_rotation

        # How far the cue should be from its center of rotation
        self.rotation_offset: int = c.MIN_ROTATION_OFFSET

        # Initialize the image
        self.image: pygame.surface = pygame.image.load("images/cue_stick.png")
        self.image = pygame.transform.scale(surface=self.image, size=(c.CUE_WIDTH, c.CUE_HEIGHT))
        self.rect: pygame.Rect = self.image.get_rect()  # Will be used to control cue movement and rotation
        self.set_rect_center(self.rotation_point)

        # Store the original image
        self.original_image = self.image

        # Set initial cue values
        self.angle: float = 0
        self.rotation_locked: bool = False
        self.movement_locked: bool = False
        self.visible: bool = True

        if c.DEBUGGING:
            # Can be used to draw a square at the center of the cue
            self.debug_center_rect = pygame.Rect(0, 0, 10, 10)
            self.debug_center_rect.center = self.rect.center

            # Can be used to draw a square at the point of rotation
            self.debug_rotation_rect = pygame.Rect(0, 0, 20, 20)
            self.debug_rotation_rect.center = (center_of_rotation.x, center_of_rotation.y)

    def rotate(self, angle: float) -> None:
        """
        Rotates the cue to a specified angle
        :param angle: The angle to rotate the cue stick to
        """
        if not self.rotation_locked:
            self.angle = angle % 360

            self.set_rect_center(self.rotation_point)

            # Rotate the cue
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect()
            self.set_rect_center(self.angle_to_point(self.angle))

            if c.DEBUGGING:
                self.debug_center_rect.center = self.rect.center

    def set_rotation_point(self, point) -> None:
        """
        Sets the rotation point for the cue stick
        :param point: The point to set to
        """
        self.rotation_point = point

    def set_position(self, position: Point):
        self.rect.x = position.x
        self.rect.y = position.y

    def set_rect_center(self, position: Point):
        self.rect.center = position.to_tuple()

    def angle_to_point(self, angle: float) -> Point:
        """
        Determines the coordinate point from the point of rotation at a given angle and a set distance
        :param angle: The angle of the point
        :return: A tuple containing the x, y coordinates of the point
        """
        delta_x = delta_y = -1
        x_pos = y_pos = 0

        angle = angle % 360

        original_x = self.rotation_point.x
        original_y = self.rotation_point.y

        quadrant_angle = math.radians(angle % 90)  # relative angle in a single quadrant from [0, 90)

        if 0 <= angle < 90 or 180 <= angle < 270:
            delta_x = self.rotation_offset * math.sin(quadrant_angle)
            delta_y = self.rotation_offset * math.cos(quadrant_angle)
        elif 90 <= angle < 180 or 270 <= angle < 360:
            delta_x = self.rotation_offset * math.cos(quadrant_angle)
            delta_y = self.rotation_offset * math.sin(quadrant_angle)

        if 0 <= angle < 90:
            x_pos = (original_x + delta_x)
            y_pos = (original_y + delta_y)
        elif 90 <= angle < 180:
            x_pos = (original_x + delta_x)
            y_pos = (original_y - delta_y)
        elif 180 <= angle < 270:
            x_pos = (original_x - delta_x)
            y_pos = (original_y - delta_y)
        elif 270 <= angle < 360:
            x_pos = (original_x - delta_x)
            y_pos = (original_y + delta_y)

        return Point(x_pos, y_pos)

    def point_to_angle(self, cursor_pos: Point):
        """
        Returns the angle of the line-segment between the center of rotation and the cursor_pos
        :param cursor_pos: The current position of the cursor
        :return: The angle, in degrees, of the line-segment
        """
        def determine_quadrant() -> int:
            """
            Determines the quadrant a line is in where the rotation point is used as the center point
            The quadrants are defined as 1:(0,90), 2:(90,180), 3:(180,270), 4:(270, 360)
            :return: The quadrant of the line
            """
            if cursor_pos.x >= self.rotation_point.x and cursor_pos.y > self.rotation_point.y:
                return 1
            elif cursor_pos.x > self.rotation_point.x and cursor_pos.y <= self.rotation_point.y:
                return 2
            elif cursor_pos.x <= self.rotation_point.x and cursor_pos.y < self.rotation_point.y:
                return 3
            elif cursor_pos.x < self.rotation_point.x and cursor_pos.y >= self.rotation_point.y:
                return 4
            else:
                # Should only be returned if something went wrong
                return -1

        # If the two points are equal return the current angle of the cue stick
        if cursor_pos.x == self.rotation_point.x and cursor_pos.y == self.rotation_point.y:
            return self.angle

        delta_x = math.fabs(cursor_pos.x - self.rotation_point.x)
        delta_y = math.fabs(cursor_pos.y - self.rotation_point.y)

        quadrant = determine_quadrant()

        quadrant_angle = None
        if quadrant == 1 or quadrant == 3:
            quadrant_angle = math.degrees(math.atan(delta_x / delta_y))
        elif quadrant == 2 or quadrant == 4:
            quadrant_angle = math.degrees(math.atan(delta_y / delta_x))

        if quadrant == 1:
            return quadrant_angle
        elif quadrant == 2:
            return quadrant_angle + 90
        elif quadrant == 3:
            return quadrant_angle + 180
        elif quadrant == 4:
            return quadrant_angle + 270

    def set_cue_power(self, cursor_pos: Point) -> bool:
        """
        Draws the cue back based on the position of the cursor
        Only sets power between the min and max offset defined in `constants.py`
        :param cursor_pos: The position of the cursor
        :return: True if the cue was set; False otherwise
        """
        def check_valid_power_mouse_pos(mouse_pos: Point) -> bool:
            """
            Determines whether a given mouse_pos is valid to pull back the cue
                by checking that the cue and mouse are not more than 45 degrees apart.
                Used to prevent mouse on opposite side of cue from moving it
            :param mouse_pos: The current position of the mouse cursor
            :return: True if the cursor is within 45 degrees of the cue stick; False otherwise
            """
            cue_angle = self.angle
            mouse_angle = self.point_to_angle(mouse_pos)

            angle_difference = math.fabs((cue_angle - mouse_angle))

            # Will return true for any angle at ±45 degrees
            if 0 <= angle_difference <= 45 or 315 <= angle_difference < 360:
                return True
            else:
                return False

        if check_valid_power_mouse_pos(cursor_pos):

            drag_distance = util.distance_formula(Point(self.rotation_point.x, self.rotation_point.y),
                                                  Point(cursor_pos.x, cursor_pos.y))

            # Causes the position that the cue is dragged at to be 1/4 from the front rather than at the middle
            drag_offset = c.CUE_HEIGHT / 4
            min_drag_distance = c.MIN_ROTATION_OFFSET - drag_offset
            max_drag_distance = c.MAX_ROTATION_OFFSET - drag_offset

            if drag_distance < min_drag_distance:
                self.rotation_offset = c.MIN_ROTATION_OFFSET
            elif min_drag_distance <= drag_distance <= max_drag_distance:
                self.rotation_offset = drag_distance + drag_offset
            elif drag_distance > max_drag_distance:
                self.rotation_offset = c.MAX_ROTATION_OFFSET

            self.set_rect_center(self.angle_to_point(self.angle))

            if c.DEBUGGING:
                self.debug_center_rect.center = self.rect.center

            return True
        else:
            return False

    def set_cue_power_to_offset(self, rotation_offset: float) -> None:
        """
        Set the cue power to a specific offset
        Only sets power between the edge of the ball and the max offset defined in `constants.py`
        :param rotation_offset: The offset to set the cue power to
        """
        if rotation_offset < c.EDGE_OF_BALL_OFFSET:
            self.rotation_offset = c.EDGE_OF_BALL_OFFSET
        elif c.EDGE_OF_BALL_OFFSET < rotation_offset < c.MAX_ROTATION_OFFSET:
            self.rotation_offset = rotation_offset
        elif rotation_offset > c.MAX_ROTATION_OFFSET:
            self.rotation_offset = c.MAX_ROTATION_OFFSET

        self.set_rect_center(self.angle_to_point(self.angle))

        if c.DEBUGGING:
            self.debug_center_rect.center = self.rect.center

    def reset_rotation(self) -> None:
        """
        Resets the rotation offset to the minimum and unlocks the rotation
        """
        self.rotation_offset = c.MIN_ROTATION_OFFSET
        self.rotation_locked = False

    def determine_cue_ball_velocity(self) -> Tuple[float, float]:
        """
        Determines the velocity that the cue ball should move at after being hit by the cue stick
            based on the cue stick's angle and the amount it was pulled back
        :return: A tuple containing the x and y components of the velocity
        """

        def split_velocity(velo_magnitude: float, velo_angle: float) -> Tuple[float, float]:
            """
            Splits a velocity vector into its directional x and y components
            :param velo_magnitude: The magnitude of the velocity vector
            :param velo_angle: The angle of the velocity vector
            :return: A tuple containing the directional x and y velocity
            """
            x_direction = y_direction = 0
            x_magnitude = y_magnitude = -1

            velo_angle = velo_angle % 360

            quadrant_angle = math.radians(velo_angle % 90)  # relative angle in a single quadrant from [0, 90)

            # Get component magnitude
            if 0 <= velo_angle < 90 or 180 <= velo_angle < 270:
                x_magnitude = velo_magnitude * math.sin(quadrant_angle)
                y_magnitude = velo_magnitude * math.cos(quadrant_angle)
            elif 90 <= velo_angle < 180 or 270 <= velo_angle < 360:
                x_magnitude = velo_magnitude * math.cos(quadrant_angle)
                y_magnitude = velo_magnitude * math.sin(quadrant_angle)

            # Get component sign
            if 0 <= velo_angle < 90:
                x_direction = -1
                y_direction = -1
            elif 90 <= velo_angle < 180:
                x_direction = -1
                y_direction = 1
            elif 180 <= velo_angle < 270:
                x_direction = 1
                y_direction = 1
            elif 270 <= velo_angle < 360:
                x_direction = 1
                y_direction = -1

            x_velo = x_direction * x_magnitude
            y_velo = y_direction * y_magnitude

            return x_velo, y_velo

        angle = self.angle % 360

        velocity = util.map_to_range(self.rotation_offset,
                                     (c.MIN_ROTATION_OFFSET, c.MAX_ROTATION_OFFSET), (0, c.MAX_CUE_BALL_VELO))

        velocity_x, velocity_y = split_velocity(velocity, angle)

        return velocity_x, velocity_y
