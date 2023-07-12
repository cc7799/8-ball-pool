import pygame

import constants as c
from constants import Point


class PoolTable(pygame.sprite.Sprite):
    def __init__(self, position: Point):
        super().__init__()

        self.image = pygame.Surface((c.SCREEN_WIDTH  - (c.SCREEN_WIDTH_PADDING * 2),
                                     c.SCREEN_HEIGHT - (c.SCREEN_HEIGHT_PADDING * 2)))

        self.image.fill(c.colors["pool_silver"])

        self.visible = True

        self.draw()

        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y

    def draw(self) -> None:
        """
        Creates the PoolTable's image
        """
        def draw_dot(pos: Point) -> None:
            """
            Draws one of the small grey dots on the pool table
            :param pos: The position of the dot
            """
            pygame.draw.circle(self.image, c.colors["pool_silver"], pos.to_tuple(), 3)

        def draw_pocket(pos: Point) -> None:
            """
            Draws one of the pockets on the pool table
            :param pos: The position of the pocket
            """
            pygame.draw.circle(self.image, c.colors["pool_black"], pos.to_tuple(), 20)

        # Draw brown background
        pygame.draw.rect(self.image, c.colors["pool_brown"],
                         pygame.Rect(0, 0, c.POOL_TABLE_WIDTH, c.POOL_TABLE_HEIGHT))
        # Draw green center background
        pygame.draw.rect(self.image, c.colors["pool_green"],
                         pygame.Rect(30, 30, c.POOL_TABLE_WIDTH - 60, c.POOL_TABLE_HEIGHT - 60))

        # Pockets #
        for horizontal_offset in (30, 400, 770):
            for vertical_offset in (30, 370):
                draw_pocket(pos=Point(horizontal_offset, vertical_offset))

        # Grey Dots #
        # Sides
        for vertical_offset in range(100, 400, 100):
            for horizontal_offset in (15, 785):
                draw_dot(pos=Point(horizontal_offset, vertical_offset))

        # Top and bottom
        for horizontal_offset in range(100, 800, 100):
            if not horizontal_offset == 400:  # Don't draw dots in the middle of the center pockets
                for vertical_offset in (15, 385):
                    draw_dot(pos=Point(horizontal_offset, vertical_offset))

        # Scorecard Boxes #
        # Brown background
        pygame.draw.rect(self.image, c.colors["pool_brown"],
                         pygame.Rect((0, c.POOL_TABLE_HEIGHT),
                                     (c.POOL_TABLE_WIDTH, c.SCREEN_HEIGHT_PADDING - 25)))

        # Line dividing board and scorecard
        pygame.draw.rect(self.image, c.colors["pool_black"],
                         pygame.Rect((0, c.POOL_TABLE_HEIGHT),
                                     (c.POOL_TABLE_WIDTH, 1)))

        # Green center background
        pygame.draw.rect(self.image, c.colors["pool_green"],
                         pygame.Rect((10, c.POOL_TABLE_HEIGHT + 10),
                                     (c.POOL_TABLE_WIDTH - 20, 80)))

        # Line dividing sections of scorecard
        pygame.draw.rect(self.image, c.colors["pool_brown"],
                         pygame.Rect((395, c.POOL_TABLE_HEIGHT + 1),
                                     (10, 90)))
