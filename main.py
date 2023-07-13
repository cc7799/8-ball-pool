import random
import sys
from typing import List, Tuple, Dict

import pygame

import constants as c
from constants import Players, GamePhases, BallTypes, Point
from cue import Cue
from pool_ball import PoolBall
from pool_ball_list import PoolBallList
from pool_table import PoolTable
import utilities as util


class GameLoop:
    def __init__(self):
        self.initialize_display()
        self.initialize_fonts()
        self.initialize_game_flags_and_trackers()
        self.initialize_sprite_groups()
        self.initialize_game_board()
        self.initialize_game_objects()

        self.clock = pygame.time.Clock()

        self.pygame_event_sets = {"action": [pygame.QUIT, pygame.MOUSEBUTTONDOWN,
                                             pygame.MOUSEBUTTONUP],
                                  "no_action": [pygame.QUIT],
                                  "debug": [pygame.QUIT] + c.DEBUG_EVENTS}

    def initialize_display(self) -> None:
        """
        Initializes the display surface
        """
        self.display_surface = pygame.display.set_mode(size=(c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.display_surface.fill(c.colors["white"])
        pygame.display.set_caption("Pool Game")

        self.background = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.background.fill(c.colors["pool_silver"])

        self.display_surface.blit(self.background, (0, 0))

    def initialize_fonts(self) -> None:
        pygame.font.init()
        self.player_text_font = pygame.font.Font(c.PLAYER_TEXT_FONT_FILENAME, c.PLAYER_TEXT_FONT_SIZE)
        self.winner_text_font = pygame.font.Font(c.WINNER_TEXT_FONT_FILENAME, c.WINNER_TEXT_FONT_SIZE)

    def initialize_sprite_groups(self) -> None:
        """
        Initializes the groups for holding the sprites
        """
        # The pool_table_sprite and cue_sprite will only contain one sprite.
        #   Groups are used because pygame provides simple methods for clearing and drawing sprites
        #   that are only able to be used on groups.
        self.pool_table_sprite: pygame.sprite.Group = pygame.sprite.Group()
        self.cue_sprite: pygame.sprite.Group = pygame.sprite.Group()

        self.pool_balls: PoolBallList = PoolBallList()

    def initialize_game_board(self) -> None:
        """
        Initializes the pool table sprite
        """
        self.pool_table: PoolTable = PoolTable(Point(c.SCREEN_WIDTH_PADDING, c.SCREEN_HEIGHT_PADDING))
        self.pool_table_sprite.add(self.pool_table)

    def initialize_game_flags_and_trackers(self) -> None:
        """
        Initializes the variables for tracking the game state
        """
        self.current_phase: GamePhases = GamePhases.place_cue

        self.current_player: Players = Players.player1

        self.player_ball_types: Dict[Players, BallTypes | None] = {Players.player1: None,
                                                                   Players.player2: None}

        self.num_balls_in: Dict[BallTypes, int] = {BallTypes.solid: 0,
                                                   BallTypes.striped: 0}

        self.winner: Players | None = None

        self.first_turn: bool = True  # Whether it's the first turn or not

        self.need_to_place_cue_ball: bool = False

        self.has_ball_gone_in_pocket: bool = False  # If a ball has gone in on the current turn

    def initialize_game_objects(self) -> None:
        """
        Initialize the cue stick and the pool balls
        """
        # Create cue ball
        self.pool_balls.add_ball(0, c.CUE_BALL_START_LOCATION)

        # Create 8-ball
        self.pool_balls.add_ball(8, c.EIGHT_BALL_START_LOCATION)

        # Create the 14 regular pool balls
        for ball_number in c.REGULAR_POOL_BALL_NUMBERS:
            ball_start_location = c.REGULAR_POOL_BALL_START_LOCATIONS.pop(
                random.randint(0, len(c.REGULAR_POOL_BALL_START_LOCATIONS) - 1))

            self.pool_balls.add_ball(ball_number, ball_start_location)

        # Create the cue stick
        self.cue: Cue = Cue(self.pool_balls.get(0).get_position())
        self.cue_sprite.add(self.cue)

    def run_game(self) -> None:
        """
        Calls the correct function for the current game phase
        """
        self.tick_frame()

        while True:
            if self.current_phase == GamePhases.place_cue:
                self.place_cue_ball_phase()
            elif self.current_phase == GamePhases.hit_cue:
                self.hit_cue_phase()
            elif self.current_phase == GamePhases.ball_in_play:
                self.ball_in_play_phase()
            elif self.current_phase == GamePhases.game_over:
                self.game_over_phase()
            elif self.current_phase == GamePhases.quit:
                self.quit_game_phase()

    def place_cue_ball_phase(self) -> None:
        """
        Controls the phase of the game where the cue ball is placed.
        Transfers to `Hit Cue` or `Quit Game` phase
        """

        def determine_cue_ball_limits() -> Dict[str, float]:
            """
            Determines the limits on where the cue ball can be placed based on whether it's the first turn
            :return: A Dictionary containing the min and max x- and y-values
            """
            limits: Dict[str, float] = {
                "max_x":
                    c.POOL_TABLE_WIDTH - 31 - (c.BALL_RADIUS * 2) + c.SCREEN_WIDTH_PADDING,
                "min_y": 30 + c.SCREEN_HEIGHT_PADDING,
                "max_y":
                    c.POOL_TABLE_HEIGHT - 31 - (c.BALL_RADIUS * 2) + c.SCREEN_HEIGHT_PADDING}

            if self.first_turn:
                self.first_turn = False

                limits["min_x"] = c.TABLE_HEAD_STRING_LOCATION
            else:
                limits["min_x"] = 30 + c.SCREEN_WIDTH_PADDING

            return limits

        def set_cue_ball_pos() -> None:
            """
            Sets the position of the cue ball to the position of the cursor within the defined position limits
            """
            cursor_pos: Point = self.get_cursor_pos()

            cursor_pos.x -= c.BALL_RADIUS  # Subtracts the ball radius to that the cursor is in the center of the ball,
            cursor_pos.y -= c.BALL_RADIUS  # rather than the top-left corner

            # Bind the cue ball to the limits
            if cursor_pos.y < pos_limits["min_y"]:
                cursor_pos.y = pos_limits["min_y"]
            elif cursor_pos.y > pos_limits["max_y"]:
                cursor_pos.y = pos_limits["max_y"]

            if cursor_pos.x < pos_limits["min_x"]:
                cursor_pos.x = pos_limits["min_x"]
            elif cursor_pos.x > pos_limits["max_x"]:
                cursor_pos.x = pos_limits["max_x"]

            self.pool_balls.get(0).set_position(cursor_pos)

        if c.DEBUGGING:
            print("[DEBUG-main.py]: starting place cue ball phase for " + str(self.current_player))

        pygame.event.set_allowed(self.pygame_event_sets["action"])

        self.need_to_place_cue_ball = False
        self.cue.visible = False
        self.pool_balls.show_ball(ball_num=0)

        pos_limits = determine_cue_ball_limits()

        while True:
            self.tick_frame()

            set_cue_ball_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.current_phase = GamePhases.quit
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.current_phase = GamePhases.hit_cue
                    self.pool_balls.get(0).in_play = True
                    return

    def hit_cue_phase(self):
        """
        Controls the phase of the game where the cue stick is aimed and fired.
        Transfers to `Ball in Play` or `Quit Game` phase
        """
        def release_cue() -> None:
            """
            Releases the cue stick and sets the velocity of the cue ball
            """
            cue_ball_velocity = self.cue.determine_cue_ball_velocity()

            # Moves the offset to touch the cue ball over a set amount of time
            current_frame = 0
            frames_to_move = seconds_to_move * c.MAX_FRAMERATE

            release_offset = self.cue.rotation_offset  # The offset when the cue was released

            change_in_offset_per_frame = (release_offset - c.EDGE_OF_BALL_OFFSET) / frames_to_move

            while current_frame < frames_to_move:
                self.cue.set_cue_power_to_offset((self.cue.rotation_offset - change_in_offset_per_frame))

                self.tick_frame()

                current_frame += 1

            # Hits the cue ball
            self.pool_balls.get(0).set_velocity(cue_ball_velocity)
            self.cue.reset_rotation()
            self.cue.visible = False

        if c.DEBUGGING:
            print("[DEBUG-main.py]: starting hit cue phase for " + str(self.current_player))

        seconds_to_move = 0.2

        pygame.event.set_allowed(self.pygame_event_sets["action"])

        # Set the cue stick to rotate around the center cue ball
        self.cue.rotation_point = Point(self.pool_balls.get(0).x_pos + c.BALL_RADIUS,
                                        self.pool_balls.get(0).y_pos + c.BALL_RADIUS)
        self.cue.visible = True

        while True:
            self.tick_frame()

            # Rotate the cue stick to follow the mouse
            cursor_pos = self.get_cursor_pos()
            cue_angle = self.cue.point_to_angle(cursor_pos)
            self.cue.rotate(cue_angle)

            # Allow the cue to be drawn back if it's been locked in place
            if self.cue.rotation_locked:
                self.cue.set_cue_power(cursor_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.current_phase = GamePhases.quit
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.cue.rotation_locked = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Only hit the cue ball if the cue stick has been pulled back
                    if self.cue.rotation_offset > c.MIN_ROTATION_OFFSET:
                        release_cue()
                        self.current_phase = GamePhases.ball_in_play
                        return
                    else:
                        self.cue.reset_rotation()

    def ball_in_play_phase(self) -> None:
        """
        Controls the phase of the game while the balls are in motion.
        Transfers to `Place Cue Ball`, `Hit Cue`, or `Quit Game` phase
        """
        def process_balls_in_pocket() -> None:
            """
            Handles any ball going in a pocket.
            Decides whether there was a winner, if the cue ball needs to be placed,
                and if the current player should be swapped.
            """
            # If any balls went in on this turn
            if len(balls_in_pocket) > 0:
                # If no balls have been hit in the entire game
                if self.num_balls_in[BallTypes.solid] == self.num_balls_in[BallTypes.striped] == 0:
                    first_ball_type = balls_in_pocket[0].type

                    # Handles if the eight-ball is the first ball in
                    if first_ball_type == BallTypes.eight:
                        self.winner = Players.swap_player(self.current_player)
                        return

                    self.player_ball_types[self.current_player] = first_ball_type
                    self.player_ball_types[Players.swap_player(self.current_player)] = BallTypes.swap_type(
                        first_ball_type)

                current_player_ball_type = self.player_ball_types[self.current_player]
                for ball in balls_in_pocket:
                    if ball.num == 0:
                        self.need_to_place_cue_ball = True
                        ball.set_velocity((0, 0))
                        self.pool_balls.hide_ball(ball_num=0)

                    elif ball.num == 8:
                        if self.num_balls_in[current_player_ball_type] == 7:
                            self.winner = self.current_player
                        else:
                            self.winner = Players.swap_player(self.current_player)

                    else:
                        ball.display_ball_below(self.num_balls_in)
                        self.num_balls_in[ball.type] += 1

        def determine_next_phase() -> GamePhases:
            """
            Determines the next phase that the game should switch to and swaps the current player if needed
            :return: The phase to switch to
            """
            # If no ball collisions happened, it means the cue ball did not hit anything
            if not any_ball_collided:
                self.need_to_place_cue_ball = True

            # Swap players if the cue ball needs to be placed or no balls have gone in
            if not self.has_ball_gone_in_pocket or self.need_to_place_cue_ball:
                self.current_player = self.current_player.swap_player()

            if self.winner is not None:
                return GamePhases.game_over

            elif self.need_to_place_cue_ball:
                return GamePhases.place_cue

            else:
                return GamePhases.hit_cue

        if c.DEBUGGING:
            pygame.event.set_allowed(self.pygame_event_sets["debug"])
            print("[DEBUG-main.py]: starting ball in play phase for " + str(self.current_player))
        else:
            pygame.event.set_allowed(self.pygame_event_sets["no_action"])

        balls_in_pocket: Tuple[PoolBall]  # A list of balls that went into a pocket on this turn
        any_ball_collided: bool = False  # Stores if any balls collided on this turn

        while True:
            self.tick_frame()

            balls_in_pocket = self.pool_balls.move_balls()
            any_ball_collided_single_step = self.pool_balls.perform_collisions()

            if any_ball_collided_single_step:
                any_ball_collided = True

            process_balls_in_pocket()

            if self.pool_balls.all_balls_stationary() or self.winner is not None:
                self.current_phase = determine_next_phase()
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.current_phase = GamePhases.quit
                    return
                # If debugging, allow key presses to count as getting the balls in the pocket.
                #   The list of key presses can be found in the README
                if c.DEBUGGING:
                    balls_in_pocket: List[PoolBall] = []
                    if event.type == pygame.KEYDOWN:
                        for key_num, digit_event_key in enumerate(c.DEBUG_EVENTS):
                            if event.key == digit_event_key:
                                key_num += 1
                                debug_ball = self.pool_balls.get(key_num)
                                if debug_ball.in_play:
                                    balls_in_pocket.append(self.pool_balls.get(key_num))
                                    process_balls_in_pocket()

    def game_over_phase(self):
        """
        Displays a screen showing the winner of the game
        Transfers to the `Quit Game` phase
        """

        if c.DEBUGGING:
            print("[DEBUG-main.py]: starting game over phase for " + str(self.current_player))

        pygame.event.set_allowed(self.pygame_event_sets["no_action"])

        self.pool_balls.hide_all_balls()
        self.pool_table.visible = False

        while True:
            self.tick_frame()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.current_phase = GamePhases.quit
                    return

    def quit_game_phase(self) -> None:
        """
        Quits the game
        Does not transfer to any other phase
        """
        if c.DEBUGGING:
            print("[DEBUG-main.py]: starting quit game phase for " + str(self.current_player))

        pygame.quit()
        sys.exit()

    def tick_frame(self) -> None:
        """
        Updates and redraws every item to the display surface
        """

        def draw_text():
            """
            Draws the text of the current player and the winner
            """
            if self.current_phase is not GamePhases.game_over:
                self.current_player_text = self.player_text_font.render(str(self.current_player),
                                                                        False,
                                                                        c.PLAYER_TEXT_COLOR)
                line_pos = util.get_text_start_position(font=self.player_text_font,
                                                        text=str(self.current_player)).to_tuple()

                self.display_surface.blit(source=self.current_player_text,
                                          dest=line_pos)
            else:
                winner_text_l1 = self.winner_text_font.render(str(self.winner),
                                                              False,
                                                              c.WINNER_TEXT_COLOR)

                winner_text_l2 = self.winner_text_font.render("WINS!",
                                                              False,
                                                              c.WINNER_TEXT_COLOR)
                line1_pos, line2_pos = util.get_text_start_position_two_lines(font=self.winner_text_font,
                                                                              line1=str(self.winner), line2="WINS!")

                self.display_surface.blit(source=winner_text_l1,
                                          dest=line1_pos.to_tuple())
                self.display_surface.blit(source=winner_text_l2,
                                          dest=line2_pos.to_tuple())

        # Draw the background to erase previous sprite positions
        self.display_surface.blit(self.background, (0, 0))

        # Draw sprites
        if self.pool_table.visible:
            self.pool_table_sprite.draw(self.display_surface)

        if self.cue.visible:
            self.cue_sprite.draw(self.display_surface)

        self.pool_balls.draw(self.display_surface)

        draw_text()

        # Update the screen
        pygame.display.flip()

        # Number of FPS
        self.clock.tick(c.MAX_FRAMERATE)

    @staticmethod
    def get_cursor_pos() -> Point:
        """
        Gets the cursor position as a point
        :return: A Point containing the current cursor position
        """
        cursor_tuple = pygame.mouse.get_pos()

        return Point(cursor_tuple[0], cursor_tuple[1])


if __name__ == "__main__":
    game = GameLoop()
    game.run_game()
