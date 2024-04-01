import pygame
from random import randint, choice
from pygame.locals import *
from enum import Enum
from player import *

# Define colors
color_path = (255, 255, 255)
color_wall = (192, 192, 192)
color_start = (255, 0, 0)
color_end = (255, 215, 0)

CELL_SIZE = 15 # Size of each cell in the maze

# Enum to represent the type of map entry
class MAP_ENTRY_TYPE(Enum):
    MAP_EMPTY = 0
    MAP_BLOCK = 1

# Enum to represent the direction of the wall
class WALL_DIRECTION(Enum):
    WALL_LEFT = 0
    WALL_UP = 1
    WALL_RIGHT = 2
    WALL_DOWN = 3

# Class to represent the maze map
class Map:
    def __init__(self, maze_level):
        self.width = maze_level
        self.height = maze_level
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]  # 2D array, 0 represents empty, 1 represents wall
        self.player = Player(1, 1)  # Initialize player at (1, 1)

    # Reset the map to all walls 
    def resetMap(self, value):
        for y in range(self.height):
            for x in range(self.width):
                self.setMap(x, y, value)

    # Set the value of the map at position (x, y) to value (0 or 1) 
    def setMap(self, x, y, value):
        if value == MAP_ENTRY_TYPE.MAP_EMPTY:
            self.map[y][x] = 0
        elif value == MAP_ENTRY_TYPE.MAP_BLOCK:
            self.map[y][x] = 1
    
    # Check if the position (x, y) is visited 
    def isVisited(self, x, y):
        return self.map[y][x] != 1

    # Draw the maze, the player and the end point on the screen 
    def drawMap(self, screen, CELL_SIZE=CELL_SIZE):
        for y in range(self.height):
            for x in range(self.width):
                color = (color_wall) if self.map[y][x] == 1 else (color_path)
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw the player
        pygame.draw.rect(screen, color_start, (self.player.x * CELL_SIZE, self.player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw the end point
        pygame.draw.rect(screen, color_end, ((self.width - 2) * CELL_SIZE, (self.height - 2) * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Check if the adjacent positions of (x, y) are visited 
def checkAdjacentPos(map, x, y, width, height, checklist):
    directions = []

    # Check left
    if x > 0 and not map.isVisited(2 * (x - 1) + 1, 2 * y + 1):
        directions.append(WALL_DIRECTION.WALL_LEFT)

    # Check up
    if y > 0 and not map.isVisited(2 * x + 1, 2 * (y - 1) + 1):
        directions.append(WALL_DIRECTION.WALL_UP)

    # Check right
    if x < width - 1 and not map.isVisited(2 * (x + 1) + 1, 2 * y + 1):
        directions.append(WALL_DIRECTION.WALL_RIGHT)

    # Check down
    if y < height - 1 and not map.isVisited(2 * x + 1, 2 * (y + 1) + 1):
        directions.append(WALL_DIRECTION.WALL_DOWN)

    if len(directions):
        direction = choice(directions)
        # Mark adjacent positions as empty
        if direction == WALL_DIRECTION.WALL_LEFT:
            map.setMap(2 * (x - 1) + 1, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
            map.setMap(2 * x, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
            checklist.append((x - 1, y))
        elif direction == WALL_DIRECTION.WALL_UP:
            map.setMap(2 * x + 1, 2 * (y - 1) + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
            map.setMap(2 * x + 1, 2 * y, MAP_ENTRY_TYPE.MAP_EMPTY)
            checklist.append((x, y - 1))
        elif direction == WALL_DIRECTION.WALL_RIGHT:
            map.setMap(2 * (x + 1) + 1, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
            map.setMap(2 * x + 2, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
            checklist.append((x + 1, y))
        elif direction == WALL_DIRECTION.WALL_DOWN:
            map.setMap(2 * x + 1, 2 * (y + 1) + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
            map.setMap(2 * x + 1, 2 * y + 2, MAP_ENTRY_TYPE.MAP_EMPTY)
            checklist.append((x, y + 1))
        return True
    else:
        return False

# Randomised Prim's algorithm to generate maze 
def randomPrim(map, width, height, screen, CELL_SIZE=CELL_SIZE):

    startX, startY = (randint(1, width - 1), randint(1, height - 1)) # random generate maze position

    # Mark start and end positionsas empty
    map.setMap(2 * startX + 1, 2 * startY + 1, MAP_ENTRY_TYPE.MAP_EMPTY)

    checklist = []  
    checklist.append((startX, startY))  
    while len(checklist): 
        entry = choice(checklist)  
        if not checkAdjacentPos(map, entry[0], entry[1], width, height, checklist):  
            # The entry has no unvisited adjacent entry, so remove it from the checklist
            checklist.remove(entry)

        # Draw the maze after each step
        map.drawMap(screen)

        pygame.display.flip()

        pygame.time.delay(1)
        
# Generate a random maze 
def doRandomPrim(map, screen):
    map.resetMap(MAP_ENTRY_TYPE.MAP_BLOCK)  # Reset map to all walls
    randomPrim(map, (map.width - 1) // 2, (map.height - 1) // 2, screen)