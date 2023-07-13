# 8 Ball Pool
This is a virtual version of an 8-ball pool billiards game

This was created as a group project for the Software Development (CS 3050) course I took as a student at UVM.

## Table of Contents
* [Description](#description)
* [Installation & Setup](#installation--setup)
* [Operation](#operation)
  * [Controls](#controls)
  * [Debug & Testing](#debug--testing)
* [Game Rules](#rules)
* [Authorship](#authorship)
* [Known Problems & Future Plans](#known-problems--future-plans)
* [Fonts Used](#fonts-used)

## Description

## Installation & Setup
The `pygame` library must be installed, which can be installed using `pip install pygame`.
No other setup is required.

## Operation
The game is started by running the `main.py` script.

### Controls
<u>Placing the Cue Ball</u>
When the cue ball needs to be placed, it will follow your cursor.
Click the left-mouse button to place the ball.

<u>Aiming and Shooting the Cue Stick</u>
Once the cue ball has been placed, the cue stick will rotate around it, following your cursor. 
Once you have found the angle of the shot you want to take, click the left mouse button and drag back.
The further back you pull, the more power your shot will have.
Release the left-mouse button when you want to fire.
If you wish to re-aim your shot, simple release the left-mouse button while the cue is drawn back at all.

### Debug & Testing
A debug mode is included for use in testing and exploring the various features of the game.
This can be enabled by changing the value of `DEBUGGING` in `constants.py`.
While debugging, various debug statements will be printed to the console.
While the balls are moving, you will also have the ability to have any ball go in a pocket using the keys
    1 – 8 for the first eight balls and q, w, e, r, t, y, u for balls 9 – 16.

Some unittesting is also included, but it is not currently comprehensive.

## Rules:
<u>Goal</u>
1. Knock the cue (white) ball into a ball of your type (striped/solid) so that the colored ball goes into a pocket.
   - The first ball to be hit in becomes the current player's ball type.
2. Once all of your balls are sunk into pockets, hit the 8-ball into a pocket.
3. If you sink the 8-ball after all your balls are in, you win; 
      however, if the 8-ball is sunk before the rest of your balls, you lose automatically.

<u>Placing the Cue Ball</u>
1. At the start of the game, the cue ball is allowed to be freely placed in the right quarter of the table 
      by the first player.
2. One subsequent turns, the cue ball starts where it ended the last turn.
3. If you knock the cue ball into one of the pockets, this is known as a scratch, and allows the other player to place
      the cue ball anywhere on the table.
4. If the cue ball does not hit another ball during your turn, this is a foul, and also allows the other player to place
      the cue ball anywhere on the table.

<u>Repeating your turn</u>
1. If you get one of your balls in, you get to repeat your turn.
2. However, if you scratched or fouled as described in the previous section, you do <i>not</i> get to repeat your turn,
      even if you got one of your balls in.

<strong>Good luck and have fun!</strong>

## Authorship
This was created as a group project and as such, not all the code was written by me. 
However, after the class was over, I refactored much of the original code, including completely rewriting `main.py`.
The complete authorship information can be found below

<table>
<tr>
    <th>File</th>
    <th>Author(s)</th>
</tr>
<tr>
    <td>constants.py</td>
    <td>All members</td>
</tr>
<tr>
    <td>cue.py</td>
    <td>Connor</td>
</tr>
<tr>
    <td>main.py</td>
    <td>Connor</td>
</tr>
<tr>
    <td>pool_ball.py</td>
    <td>Other group members</td>
</tr>
<tr>
    <td>pool_ball_list.py</td>
    <td>Connor</td>
</tr>
<tr>
    <td>pool_table.py</td>
    <td>Other group members</td>
</tr>
<tr>
    <td>unit_testing.py</td>
    <td>Connor</td>
</tr>
<tr>
    <td>utilities.py</td>
    <td>Connor</td>
</tr>
</table>


## Known Problems & Future Plans
### Known Problems
1. Collisions seem to impart more energy to balls than they should

### Future Plans
<u>Game Changes</u>
1. Implement a computer player
2. Add text showing which ball type is for which player
3. Add ability to play game again without re-running script
4. Add starting menu
5. Add minor magnetization effect to pockets to simulate how real pool balls can fall into a pocket
   - Would help reduce difficulty in getting a ball into a pocket

<u>Refactoring</u>
1. Finish the implementation of unittests
2. Set all spacing values to be based on the screen height and width to allow for resizing the window
3. Automatically clear the image of a sprite when it's set to be hidden to avoid having to check for visibility
    when drawing



## Fonts Used
The font files used in this project are `abduction2002` and `Arcade` from `1001freefonts.com`.