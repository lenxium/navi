from enum import Enum

# Enumeration for player directions
class PLAYER_DIRECTION(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

# Class to represent the player
class Player:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y

    # Function to move the player in the specified direction, updating the player's position if possible
    def move(self, direction):
        if direction == PLAYER_DIRECTION.UP:
            self.y -= 1
        elif direction == PLAYER_DIRECTION.DOWN:
            self.y += 1
        elif direction == PLAYER_DIRECTION.LEFT:
            self.x -= 1
        elif direction == PLAYER_DIRECTION.RIGHT:
            self.x += 1

# Function to move the player in the specified direction if possible (i.e. if the new position is within the maze boundaries and is a valid path)
def move_player(map, direction):
    new_x, new_y = map.player.x, map.player.y

    if direction == PLAYER_DIRECTION.UP:
        new_y -= 1
    elif direction == PLAYER_DIRECTION.DOWN:
        new_y += 1
    elif direction == PLAYER_DIRECTION.LEFT:
        new_x -= 1
    elif direction == PLAYER_DIRECTION.RIGHT:
        new_x += 1

    # Check if the new position is within the maze boundaries and is a valid path
    if 0 <= new_x < map.width and 0 <= new_y < map.height and map.map[new_y][new_x] == 0:
        map.player.move(direction)