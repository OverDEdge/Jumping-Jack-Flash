# Jumping-Jack-Flash
A simple platform game in Python using Pygame. 
Necassary packages:
- Pygame

## Aim of the game
Goal is to get as high as possible where points are awarded when platforms despawn at the bottom of the screen. 

## Game Mechanics
**Movement**

Move left and right using the ARROW keys. Left and Right Screen-wrap is implemented.
Jump using SPACE or UP key. Double jump is possible and holding jump key will cause jump to be higher.

**Death**

Death occurs if character falls down below bottom of the screen or if collide with enemy

**Score**

Platforms and enemies spawn at random heights. The higher up you go the more enemies are spawned.

**Collisions**

Game character will collide with platforms (not going through).

**Highscore**

A Highscore will be saved and displayed at Game Over and Start Screen. Hihscore can be reset by deleting contents of 'highscore.txt' file.

## How to start the game
Download a copy of the repository into a folder. Navigate and enter folder. In Command Prompt type: 
- **python -m Jumping_Jack_Flash**

This will start the game and game will launch in Fullscreen mode and 'ESC' can be used to exit.

## Art
Art has been taken from OpenGameArt.org and contributions are mentioned in the 'main.py' file.

