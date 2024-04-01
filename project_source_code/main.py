import pygame, sys, sqlite3, traceback, random 
from pygame.locals import *
from maze import *
from player import *
from pathfinder import *
import authentication
import game_level_interface

# Initialise pygame
pygame.init()
pygame.display.set_caption('NAVI')
screen = pygame.display.set_mode((645, 970))
pygame.mixer.init()

# Define fonts
font_large = pygame.font.Font('font/Comfortaa_Bold.ttf', 80)
font_medium = pygame.font.Font('font/Comfortaa_Regular.ttf', 40)
font_small = pygame.font.Font(None, 20)

# Define colors
color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_grey = (192, 192, 192)
color_red = (255, 0, 0)
color_light_grey = (211, 211, 211)

size = width,height = 645, 970
level = 11;

# Define icon
icon = pygame.image.load('resources/image/icon.png')
pygame.display.set_icon(icon)

# Sound effects
sound_button = pygame.mixer.Sound('resources/sound/button.mp3')
sound_button.set_volume(1)
sound_move = pygame.mixer.Sound('resources/sound/move.mp3')
sound_move.set_volume(2)
sound_next = pygame.mixer.Sound('resources/sound/next.mp3')
sound_next.set_volume(0.5)
sound_reach = pygame.mixer.Sound('resources/sound/reach.mp3')
sound_reach.set_volume(1)
sound_clap = pygame.mixer.Sound('resources/sound/clap.mp3')
sound_clap.set_volume(0.5)

# Draw the button
def drawButton(screen, rect, text, font, text_color, button_color, button_size=None):
    # Draw the button surface
    button_surface = pygame.Surface((button_size[0], button_size[1])) if button_size else pygame.Surface(rect.size)
    button_surface.fill(button_color)
    # Draw the button border
    pygame.draw.rect(button_surface, color_black, (0, 0, button_surface.get_width(), button_surface.get_height()), 2)
    # Draw the text on the button
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(button_surface.get_width() / 2, button_surface.get_height() / 2))
    # Blit the text on the button
    button_surface.blit(text_surface, text_rect)
    screen.blit(button_surface, rect)

def main():
    # Connect to SQLite database (or create it if not exists)
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    # Create a table to store user information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            level INT DEFAULT 1
        )
    ''')
    # Commit changes and close the database connection
    conn.commit()
    conn.close()

    generate_maze = False # Variable to control maze generation

    # Main menu text
    text_game_main_status = font_small.render(u'v1.1.6', True, color_black)
    text_game_main_status_rect = text_game_main_status.get_rect(center=(screen.get_rect().centerx + 200, screen.get_rect().centery - 200))

    # Main menu logo
    image_main_menu = pygame.image.load('resources/image/main_menu.png').convert()
    image_main_menu_rect = image_main_menu.get_rect(center=(screen.get_rect().centerx, screen.get_rect().centery - 300))

    # Medal image
    image_medal = pygame.image.load('resources/image/medal.png').convert_alpha()
    image_medal_rect = image_medal.get_rect(center=(screen.get_rect().centerx, screen.get_rect().centery - 200))

    # Play button
    button_play_rect = pygame.Rect(0, 0, 200, 60)
    button_play_rect.center = (screen.get_rect().centerx, screen.get_rect().centery - 100)
    drawButton(screen, button_play_rect, 'Play', font_medium, color_black, color_grey)

    # Login button
    button_login_rect = pygame.Rect(0, 0, 200, 60)
    button_login_rect.center = (screen.get_rect().centerx, screen.get_rect().centery)
    drawButton(screen, button_login_rect, 'Login', font_medium, color_black, color_grey)

    # Register button
    button_register_rect = pygame.Rect(0, 0, 200, 60)
    button_register_rect.center = (screen.get_rect().centerx, screen.get_rect().centery+100)
    drawButton(screen, button_register_rect, 'Register', font_medium, color_black, color_grey)

    # Next Level button
    button_next_rect = pygame.Rect(0, 0, 200, 60)
    button_next_rect.center = (screen.get_rect().centerx, screen.get_rect().centery)

    # Regenerate button
    button_regenerate_rect = pygame.Rect(0, 0, 100, 40)
    button_regenerate_rect.center = (screen.get_rect().centerx - 270, screen.get_rect().centery +182)

    # return button
    button_return_rect = pygame.Rect(0, 0, 100, 40)
    button_return_rect.center = (screen.get_rect().centerx +270, screen.get_rect().centery +182)

    # Previous Level button
    button_previous_rect = pygame.Rect(0, 0, 100, 40)
    button_previous_rect.center = (screen.get_rect().centerx - 168, screen.get_rect().centery + 182)

    # Skip button
    button_skip_rect = pygame.Rect(0, 0, 100, 40)
    button_skip_rect.center = (screen.get_rect().centerx-66, screen.get_rect().centery + 182)

    # DFS button
    button_dfs_rect = pygame.Rect(0, 0, 100, 40)
    button_dfs_rect.center = (screen.get_rect().centerx - 270, screen.get_rect().centery + 224)

    # BFS button
    button_bfs_rect = pygame.Rect(0, 0, 100, 40)
    button_bfs_rect.center = (screen.get_rect().centerx - 168, screen.get_rect().centery + 224)

    # Dijkstra button
    button_dijkstra_rect = pygame.Rect(0, 0, 100, 40)
    button_dijkstra_rect.center = (screen.get_rect().centerx - 66, screen.get_rect().centery + 224)

    # A* button
    button_astar_rect = pygame.Rect(0, 0, 100, 40)
    button_astar_rect.center = (screen.get_rect().centerx + 36, screen.get_rect().centery + 224)

    # Return to main menu button
    return_main_text = font_medium.render('Return', True, color_red)
    return_main_text_rect = return_main_text.get_rect(center=(screen.get_rect().centerx + 213, screen.get_rect().centery + 182))

    # Maze setup
    maze_min_level = 11
    maze_max_level = 43
    maze_level = maze_min_level
    maze = Map(maze_level) 
    maze.drawMap(screen)

    # Clear the DFS path
    dfs_path = set()
    bfs_path = set() 
    dijkstra_path = set()
    astar_path = set()
    
    # Game states
    game_main_status = 0
    game_level_interface_status = 30
    user, level = None, None
    Gamestate = game_main_status

    # Sentences for winning
    sentences = [
        'You Win!',
        'Well Played!',
        'Marvellous!',
        'Congratulations!',
        'Phenomenal!',
        'Spectacular!',
        'Brilliant Victory!'
    ]   
    
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                save_level_db(user, level)
                sys.exit()

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load('resources/bgm/0.wav')
                pygame.mixer.music.play(-1, 0.0)

            # Mouse click event
            if Gamestate == game_main_status:
                if user is None:
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1 and button_play_rect.collidepoint(event.pos):
                                if user is None:
                                    Gamestate = 11
                                    maze_level = min(maze_level + 2, maze_max_level)
                                    maze = Map(maze_level)        
                                    maze.resetMap(MAP_ENTRY_TYPE.MAP_BLOCK)
                                    generate_maze = True
                                    dfs_path = set()
                                    bfs_path = set() 
                                    dijkstra_path = set()
                                    astar_path = set()            
                                    sound_next.play() 
                                else:
                                    Gamestate = game_level_interface_status
                                    sound_button.play()
                        elif event.button ==1 and button_login_rect.collidepoint(event.pos):
                            Gamestate = 21 # Login
                            sound_button.play()
                        elif event.button ==1 and button_register_rect.collidepoint(event.pos):
                            Gamestate = 22 # Register
                            sound_button.play()
                    screen.fill(color_white)
                    screen.blit(image_main_menu, image_main_menu_rect)
                    screen.blit(text_game_main_status, text_game_main_status_rect)
                    drawButton(screen, button_play_rect, 'Play', font_medium, color_black, color_grey)
                    drawButton(screen, button_login_rect, 'Login', font_medium, color_black, color_grey)
                    drawButton(screen, button_register_rect, 'Register', font_medium, color_black, color_grey)
                else:
                    # Display the secondary menu for logged in users
                    button_logout_rect = pygame.Rect(0, 0, 200, 60)
                    button_logout_rect.center = (screen.get_rect().centerx, screen.get_rect().centery)

                    if event.type == MOUSEBUTTONDOWN and button_play_rect.collidepoint(event.pos):
                        Gamestate = game_level_interface_status
                        sound_button.play()
                    elif event.type == MOUSEBUTTONDOWN and button_logout_rect.collidepoint(event.pos):
                        save_level_db(user, level) # Save the current level of the user to the database
                        user, level = None, None # Logout the user
                        screen.fill(color_white)
                        drawButton(screen, button_play_rect, 'Play', font_medium, color_black, color_grey)
                        drawButton(screen, button_login_rect, 'Login', font_medium, color_black, color_grey)
                        drawButton(screen, button_register_rect, 'Register', font_medium, color_black, color_grey)
                        continue
                    # Draw main menu interface
                    screen.fill(color_white)
                    screen.blit(image_main_menu, image_main_menu_rect)
                    screen.blit(text_game_main_status, text_game_main_status_rect)

                    drawButton(screen, button_play_rect, 'Continue', font_medium, color_black, color_grey)
                    drawButton(screen, button_logout_rect, 'Logout', font_medium, color_black, color_grey)

            if Gamestate == 21: # Login
                Gamestate, user = authentication.handle_login_events(game_main_status=game_main_status, 
                                                Gamestate_code = [game_level_interface_status],
                                                win_size=size)
                if user is not None:
                    level = query_db_level(user=user) # Get the current level of the user from the database
            
            if Gamestate == 22: # Register
                Gamestate, user = authentication.handle_register_events(game_main_status=game_main_status, 
                Gamestate_code = [game_level_interface_status], 
                                                win_size=size,
                                                is_register=True)
                if user is not None:
                    level = query_db_level(user=user)
            
            if Gamestate == game_level_interface_status:
                game_level_interface_cls = game_level_interface.GameLevelInterface(
                                                               win_size=size,
                                                                game_status_code = [game_main_status, 11],
                                                               screen=screen,
                                                               user=user,
                                                               level=level,
                                                               return_main_text=(return_main_text_rect, return_main_text),
                                                               common_methond=(common_ui,[user, screen, return_main_text, return_main_text_rect]))
                Gamestate = game_level_interface_cls.deal()

                # If the user has selected a level, then start the game
                if isinstance(Gamestate, list) and len(Gamestate) == 2:
                    new_game_state, selected_level = Gamestate

                    if new_game_state == 11:
                        # Convert the selected level to an odd number for the maze generation
                        maze_level = max(min(selected_level, maze_max_level), maze_min_level)
                        if maze_level % 2 == 0:
                            maze_level += 1  # Make sure the maze level is odd

                        screen.fill(color_white)
                        maze = Map(maze_level)
                        common_ui(user, screen, return_main_text, return_main_text_rect)
                        generate_maze = True
                        Gamestate = 18         

            if Gamestate == 11: # Gamestate for maze generation and pathfinding
                # Draw the maze
                if generate_maze:
                    screen.fill(color_white)
                    doRandomPrim(maze,screen)                                    
                    generate_maze = False  # Reset the flag to prevent continuous maze generation 
                    Gamestate = 18
                    common_ui(user, screen, return_main_text, return_main_text_rect)
                    drawButton(screen, button_regenerate_rect, 'Regenerate', font_small, color_black, color_grey, button_size=(100, 40))  
                    drawButton(screen, button_previous_rect, 'Previous Level', font_small, color_black, color_grey, button_size=(100, 40)) 
                    drawButton(screen, button_skip_rect, 'Skip', font_small, color_black, color_grey, button_size=(100, 40))

                    drawButton(screen, button_dfs_rect, 'DFS', font_small, color_black, color_grey, button_size=(100, 40))
                    drawButton(screen, button_bfs_rect, 'BFS', font_small, color_black, color_grey, button_size=(100, 40))
                    drawButton(screen, button_dijkstra_rect, 'Dijkstra', font_small, color_black, color_grey, button_size=(100, 40))
                    drawButton(screen, button_astar_rect, 'A*', font_small, color_black, color_grey, button_size=(100, 40))    

                maze.drawMap(screen) # Draw the maze on the screen
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button_regenerate_rect.collidepoint(event.pos): # Regenerate the maze and reset the path
                            dfs_path = set()
                            bfs_path = set() 
                            dijkstra_path = set()
                            astar_path = set() 
                            generate_maze = True
                            maze.resetMap(MAP_ENTRY_TYPE.MAP_BLOCK)
                            sound_button.play()

                        if button_previous_rect.collidepoint(event.pos): 
                            maze_level = max(maze_level - 2, maze_min_level)  # choose the level between 11 and 43, the level is odd
                            maze = Map(maze_level)
                            maze.resetMap(MAP_ENTRY_TYPE.MAP_BLOCK)
                            dfs_path = set()
                            bfs_path = set() 
                            dijkstra_path = set()
                            astar_path = set() 
                            generate_maze = True
                            sound_button.play()

                        if button_skip_rect.collidepoint(event.pos): 
                            selected_sentence = sentences[random.randint(0, len(sentences) - 1)]  # Randomly select a congrats sentence from the list
                            sound_reach.play()                          
                            dfs_path = set()
                            bfs_path = set() 
                            dijkstra_path = set()
                            astar_path = set() 
                            Gamestate = 100 # Gamestate for winning
                            
                        if button_return_rect.collidepoint(event.pos):
                            Gamestate = game_main_status
                            sound_button.play()
                            dfs_path = set()
                            bfs_path = set() 
                            dijkstra_path = set()
                            astar_path = set() 
                            continue

                        # Check if the mouse click is within the maze area
                        if (maze.player.x, maze.player.y) in dfs_path:
                            pygame.draw.rect(screen, color_red, (maze.player.x * CELL_SIZE, maze.player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        if (maze.player.x, maze.player.y) in bfs_path:
                            pygame.draw.rect(screen, color_red, (maze.player.x * CELL_SIZE, maze.player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        if (maze.player.x, maze.player.y) in dijkstra_path:
                            pygame.draw.rect(screen, color_red, (maze.player.x * CELL_SIZE, maze.player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        if (maze.player.x, maze.player.y) in astar_path:
                            pygame.draw.rect(screen, color_red, (maze.player.x * CELL_SIZE, maze.player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                        if button_dfs_rect.collidepoint(event.pos):
                            Gamestate = 12
                            sound_button.play()
                        if button_bfs_rect.collidepoint(event.pos):
                            Gamestate = 13
                            sound_button.play()
                        if button_dijkstra_rect.collidepoint(event.pos):
                            Gamestate = 14
                            sound_button.play()
                        if button_astar_rect.collidepoint(event.pos):
                            Gamestate = 15
                            sound_button.play()

                elif event.type == KEYDOWN:
                    if event.key == K_UP or event.key == K_w:
                        move_player(maze, PLAYER_DIRECTION.UP)
                        sound_move.play()
                    elif event.key == K_DOWN or event.key == K_s:
                        move_player(maze, PLAYER_DIRECTION.DOWN)
                        sound_move.play()
                    elif event.key == K_LEFT or event.key == K_a:
                        move_player(maze, PLAYER_DIRECTION.LEFT)
                        sound_move.play()
                    elif event.key == K_RIGHT or event.key == K_d:
                        move_player(maze, PLAYER_DIRECTION.RIGHT)  
                        sound_move.play() 
                
                # Check if the player has reached the goal
                if maze.player.x == maze.width - 2 and maze.player.y == maze.height - 2:
                    sound_reach.play()
                    selected_sentence = sentences[random.randint(0, len(sentences) - 1)]
                    Gamestate = 100

            if Gamestate == 18: # Gamestate for maze generation and pathfinding
                # Placeholder values for the table
                dfs_nodes_visited, dfs_path_length, dfs_execution_time = dataDFS(maze, (maze.player.x, maze.player.y), (maze.width - 2, maze.height - 2))
                bfs_nodes_visited, bfs_path_length, bfs_execution_time = dataBFS(maze, (maze.player.x, maze.player.y), (maze.width - 2, maze.height - 2))
                dij_nodes_visited, dij_path_length, dij_execution_time = dataDijkstra(maze, (maze.player.x, maze.player.y), (maze.width - 2, maze.height - 2))
                astar_nodes_visited, astar_path_length, astar_execution_time = dataAStar(maze, (maze.player.x, maze.player.y), (maze.width - 2, maze.height - 2))

                # Draw the table with placeholder values
                text_type = font_small.render('      Path Length                        Nodes Visited                        Execution Time (ms)', True, color_black)
                text_result1 = font_small.render('DFS                ' + str(dfs_path_length).zfill(3) + '                                        ' 
                                                 + str(dfs_nodes_visited).zfill(3) + '                                         ' 
                                                 + format(dfs_execution_time, '.3g'), True, color_black
                                                 )
                text_result2 = font_small.render('BFS                ' 
                                                 + str(bfs_path_length).zfill(3) + '                                        ' 
                                                 + str(bfs_nodes_visited).zfill(3) + '                                         ' 
                                                 + format(bfs_execution_time, '.3g'), True, color_black
                                                 )
                text_result3 = font_small.render('DIJ                  ' + str(dij_path_length).zfill(3) 
                                                 + '                                        ' 
                                                 + str(dij_nodes_visited).zfill(3) 
                                                 + '                                         ' 
                                                 + format(dij_execution_time, '.3g'), True, color_black
                                                 )
                text_result4 = font_small.render('A*S                 ' 
                                                 + str(astar_path_length).zfill(3) 
                                                 + '                                        ' 
                                                 + str(astar_nodes_visited).zfill(3) 
                                                 + '                                         ' 
                                                  + format(astar_execution_time, '.3g'), True, color_black
                                                 )

                # Adjust the positions for visibility
                screen.blit(text_type, (90, 760))
                screen.blit(text_result1, (50, 800))
                screen.blit(text_result2, (50, 840))
                screen.blit(text_result3, (50, 880))
                screen.blit(text_result4, (50, 920))

                Gamestate = 11
    
            if Gamestate == 12: # Gamestate for DFS pathfinding
                dfs_path = searchDFS(maze, (maze.player.x, maze.player.y), (maze.width - 2, maze.height - 2), screen)  # Added screen parameter
                Gamestate = 11
            if Gamestate == 13: # Gamestate for BFS pathfinding
                bfs_path = searchBFS(maze, (maze.player.x, maze.player.y), (maze.width - 2, maze.height - 2), screen)
                Gamestate = 11
            if Gamestate == 14: # Gamestate for Dijkstra pathfinding
                dijkstra_path = searchDijkstra(maze, (maze.player.x, maze.player.y), (maze.width - 2, maze.height - 2), screen)
                Gamestate = 11
            if Gamestate == 15: # Gamestate for A* pathfinding
                astar_path = searchAStar(maze, (maze.player.x, maze.player.y), (maze.width - 2, maze.height - 2), screen) 
                Gamestate = 11
            
            if Gamestate == 100: # Gamestate for winning
                sound_clap.play()
                screen.fill(color_white)

                # Randomly select a sentence
                text_win = font_large.render(selected_sentence, True, color_black)

                text_win_rect = text_win.get_rect(center=(screen.get_rect().centerx, screen.get_rect().centery - 400))
                screen.blit(text_win, text_win_rect)
                screen.blit(image_medal, image_medal_rect)
                drawButton(screen, button_next_rect, 'Next Level', font_medium, color_black, color_grey, button_size=(200, 60))
                common_ui(user, screen, return_main_text, return_main_text_rect)

                if event.type == MOUSEBUTTONDOWN:
                    sound_clap.stop()
                    if event.button == 1 and button_next_rect.collidepoint(event.pos):
                        Gamestate = 11
                        if user is not None:
                            level += 1
                            save_level_db(user, level)
                        pygame.mixer.music.stop()
                        if not pygame.mixer.music.get_busy():
                            sound_next.play()
                            pygame.mixer.music.load('resources/bgm/%s.wav' % random.randint(0, 10))
                            pygame.mixer.music.set_volume(1.5)
                            pygame.mixer.music.play(-1, 0.0)
                            
                        maze_level = min(maze_level + 2, maze_max_level)
                        maze = Map(maze_level)        
                        maze.resetMap(MAP_ENTRY_TYPE.MAP_BLOCK)
                        generate_maze = True
                        dfs_path = set()
                        bfs_path = set() 
                        dijkstra_path = set()
                        astar_path = set()            
                        sound_button.play()  
                    if event.button == 1 and button_return_rect.collidepoint(event.pos):
                        Gamestate = game_main_status
                        sound_button.play()
                        dfs_path = set()
                        bfs_path = set() 
                        dijkstra_path = set()
                        astar_path = set() 
                        continue  
    
        # Draw the shortest path in red
        for position in dfs_path:
            pygame.draw.rect(screen, color_red, (position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for position in bfs_path:
            pygame.draw.rect(screen, color_red, (position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for position in dijkstra_path:
            pygame.draw.rect(screen, color_red, (position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for position in astar_path:  
            pygame.draw.rect(screen, color_red, (position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Update screen
        pygame.display.update()
        # Tick clock
        pygame.time.Clock().tick(60)

# Common UI for all game states except the main menu and login/register interface 
def common_ui(user, screen:pygame.Surface, 
              return_main_text:pygame.Surface, 
              return_main_text_rect:Rect):
    screen.blit(return_main_text, return_main_text_rect)
    if user is None:
        user = 'Visitor!not login'
    else:
        user += '! logged in'
    margin = 2
    user_text_surface = font_small.render(user , True, (color_black))
    user_text_rect = user_text_surface.get_rect()
    user_text_rect.center = (return_main_text_rect.center[0], 
                             return_main_text_rect.bottom+user_text_rect.height//2 +margin)
    screen.blit(user_text_surface, user_text_rect) 

# Query the database to get the current level of the user 
def query_db_level(user):
    with sqlite3.connect('user_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT level FROM users WHERE username=?', (user,))
        level = cursor.fetchone()
        return level[0]
    
# Save the current level of the user to the database 
def save_level_db(user, level):
    with sqlite3.connect('user_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('update users SET level=? WHERE username=?', (level, user))
        conn.commit()

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc() # Print the traceback to the console
        pygame.quit() 
        input() # Wait for the user to press enter before closing the window