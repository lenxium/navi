import pygame, sys, heapq, time
from enum import Enum
from pygame.locals import *

color_red = (255, 0, 0)

CELL_SIZE = 15

# Enumeration for player directions (used in player.py)
class DIRECTION(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

# Depth-First Search algorithm for maze solving
def searchDFS(maze, start, end, screen, delay=30):
    stack = [(start, [])]
    visited = set() 

    while stack:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        current_position, path = stack.pop()
        x, y = current_position

        if current_position == end:
            return set(path + [current_position])

        if current_position not in visited:
            visited.add(current_position)

            for direction in DIRECTION:
                new_x, new_y = x + direction.value[0], y + direction.value[1]

                if 0 <= new_x < maze.width and 0 <= new_y < maze.height and maze.map[new_y][new_x] == 0:
                    stack.append(((new_x, new_y), path + [current_position]))

                    # Visualize the process by drawing the maze and the current path
                    maze.drawMap(screen)
                    for position in path + [current_position]:
                        pygame.draw.rect(screen, color_red, (position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                    # Delay to slow down visualization (in milliseconds)
                    pygame.time.delay(delay)
                    # Update display
                    pygame.display.flip()
    return set()  # No path found
 
def searchBFS(maze, start, end, screen, delay=30):
    queue = [(start, [])]
    visited = set()

    while queue:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        current_position, path = queue.pop(0)
        x, y = current_position

        if current_position == end:
            return set(path + [current_position])

        if current_position not in visited:
            visited.add(current_position)

            for direction in DIRECTION:
                new_x, new_y = x + direction.value[0], y + direction.value[1]

                if 0 <= new_x < maze.width and 0 <= new_y < maze.height and maze.map[new_y][new_x] == 0:
                    queue.append(((new_x, new_y), path + [current_position]))

                    # Visualize the process by drawing the maze and the current path
                    maze.drawMap(screen)
                    for position in path + [current_position]:
                        pygame.draw.rect(screen, color_red, (position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                    # Update display
                    pygame.display.flip()

                    # Delay to slow down visualization (in milliseconds)
                    pygame.time.delay(delay)

    return set()  # No path found

def searchDijkstra(maze, start, end, screen, delay=30):
    priority_queue = [(0, start, [])]
    visited = set()

    while priority_queue:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        cost, current_position, path = heapq.heappop(priority_queue)
        x, y = current_position

        if current_position == end:
            return set(path + [current_position])

        if current_position not in visited:
            visited.add(current_position)

            for direction in DIRECTION:
                new_x, new_y = x + direction.value[0], y + direction.value[1]

                if 0 <= new_x < maze.width and 0 <= new_y < maze.height and maze.map[new_y][new_x] == 0:
                    new_cost = cost + 1  # Uniform cost for each move

                    heapq.heappush(priority_queue, (new_cost, (new_x, new_y), path + [current_position]))

                    # Visualize the process by drawing the maze and the current path
                    maze.drawMap(screen)
                    for position in path + [current_position]:
                        pygame.draw.rect(screen, color_red, (position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                    # Update display
                    pygame.display.flip()

                    # Delay to slow down visualization (in milliseconds)
                    pygame.time.delay(delay)

    return set()  # No path found

def heuristic(node, goal):
    # A simple Manhattan distance heuristic for A*
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def searchAStar(maze, start, end, screen, delay=30):
    priority_queue = [(0, start, [])]
    visited = set()

    while priority_queue:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        cost, current_position, path = heapq.heappop(priority_queue)
        x, y = current_position

        if current_position == end:
            return set(path + [current_position])

        if current_position not in visited:
            visited.add(current_position)

            for direction in DIRECTION:
                new_x, new_y = x + direction.value[0], y + direction.value[1]

                if 0 <= new_x < maze.width and 0 <= new_y < maze.height and maze.map[new_y][new_x] == 0:
                    new_cost = cost + 1  # Uniform cost for each move
                    heuristic_cost = heuristic((new_x, new_y), end)

                    heapq.heappush(priority_queue, (new_cost + heuristic_cost, (new_x, new_y), path + [current_position]))

                    # Visualize the process by drawing the maze and the current path
                    maze.drawMap(screen)
                    for position in path + [current_position]:
                        pygame.draw.rect(screen, color_red, (position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                    # Update display
                    pygame.display.flip()

                    # Delay to slow down visualization (in milliseconds)
                    pygame.time.delay(delay)

    return set()  # No path found

def dataDFS(maze, start, end):
    start_time = time.time()  # Start time measurement
    stack = [(start, [])]
    visited = set()
    nodes_explored = 0

    while stack:
        current_position, path = stack.pop()
        x, y = current_position

        if current_position == end:
            end_time = time.time()
            time_taken = (end_time - start_time) * 1000  # Convert to milliseconds
            return  nodes_explored, len(path), time_taken

        if current_position not in visited:
            visited.add(current_position)
            nodes_explored += 1  # Increment nodes explored

            for direction in DIRECTION:
                new_x, new_y = x + direction.value[0], y + direction.value[1]

                if 0 <= new_x < maze.width and 0 <= new_y < maze.height and maze.map[new_y][new_x] == 0:
                    stack.append(((new_x, new_y), path + [current_position]))

    time_taken = (time.time() - start_time) * 1000
    return 0, 0, time_taken  # No path found

def dataBFS(maze, start, end):
    start_time = time.time()  # Start time measurement
    queue = [(start, [])]
    visited = set()
    nodes_explored = 0

    while queue:
        current_position, path = queue.pop(0)
        x, y = current_position

        if current_position == end:
            end_time = time.time()
            time_taken = (end_time - start_time) * 1000  # Convert to milliseconds
            return nodes_explored, len(path), time_taken

        if current_position not in visited:
            visited.add(current_position)
            nodes_explored += 1  # Increment nodes explored

            for direction in DIRECTION:
                new_x, new_y = x + direction.value[0], y + direction.value[1]

                if 0 <= new_x < maze.width and 0 <= new_y < maze.height and maze.map[new_y][new_x] == 0:
                    queue.append(((new_x, new_y), path + [current_position]))

    time_taken = (time.time() - start_time) * 1000
    return 0, 0, time_taken  # No path found

def dataDijkstra(maze, start, end):
    start_time = time.time()  # Start time measurement
    priority_queue = [(0, start, [])]
    visited = set()
    nodes_explored = 0

    while priority_queue:
        cost, current_position, path = heapq.heappop(priority_queue)
        x, y = current_position

        if current_position == end:
            end_time = time.time()
            time_taken = (end_time - start_time) * 1000
            return nodes_explored, len(path), time_taken

        if current_position not in visited:
            visited.add(current_position)
            nodes_explored += 1  # Increment nodes explored

            for direction in DIRECTION:
                new_x, new_y = x + direction.value[0], y + direction.value[1]

                if 0 <= new_x < maze.width and 0 <= new_y < maze.height and maze.map[new_y][new_x] == 0:
                    new_cost = cost + 1  # Uniform cost for each move

                    heapq.heappush(priority_queue, (new_cost, (new_x, new_y), path + [current_position]))

    time_taken = (time.time() - start_time) * 1000
    return 0, 0, time_taken  # No path found

def dataAStar(maze, start, end):
    start_time = time.time()  # Start time measurement
    priority_queue = [(0, start, [])]
    visited = set()
    nodes_explored = 0

    while priority_queue:
        cost, current_position, path = heapq.heappop(priority_queue)
        x, y = current_position

        if current_position == end:
            end_time = time.time()
            time_taken = (end_time - start_time) * 1000  # Convert to milliseconds
            return nodes_explored, len(path), time_taken

        if current_position not in visited:
            visited.add(current_position)
            nodes_explored += 1  # Increment nodes explored

            for direction in DIRECTION:
                new_x, new_y = x + direction.value[0], y + direction.value[1]

                if 0 <= new_x < maze.width and 0 <= new_y < maze.height and maze.map[new_y][new_x] == 0:
                    new_cost = cost + 1  # Uniform cost for each move
                    heuristic_cost = heuristic((new_x, new_y), end)

                    heapq.heappush(priority_queue, (new_cost + heuristic_cost, (new_x, new_y), path + [current_position]))

    time_taken = (time.time() - start_time) * 1000
    return 0, 0, time_taken  # No path found
