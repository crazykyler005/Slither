# Slither

## Description

This application is a clone of snake written in pygame which was made to get familiar with aspects of game design and the pygame library by creating a simplistic game.

The game utilizes the python game library pygame, random number generator and keyboard input. It's based off the well known game Snake and the objective is to see how long a controlled snake grows by eating apples, which are spawned in at random locations, before you collide into your self or the edges of the screen. Features include pause fuctionality, a score which is constantly updated, a high score which is saved and loaded upon exit and launch of the game, and two different interfaces for starting and restarting the game.

## Change Log
### v1.2.0
- added a high score to game over screen
- the score text while playing only increases size when a new high score is achieved
- Fixed snake tail being at wrong angle when multiple directional inputs are pushed before a single frame

### v1.1.1
- fixed edge-case with boundary at (x,0) and (0,y)
- added version number in game intro screen
- version number will auto-increment when making new build
- increased length of snake by 1 at start
- changed initial game pace to be slower but pace now slowly increases for every 10 points

### v1.1.0
- added grid layout to game with alpha level transparency added to the grid color
- added toggle functionality to grid
