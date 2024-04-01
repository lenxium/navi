import pygame, sys, sqlite3

# Define colors
color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_grey = (192, 192, 192)
color_red = (255, 0, 0)
color_light_grey = (211, 211, 211)

# Define the level object class, used to display the level button 
class LevelObject(pygame.sprite.Sprite):
    def __init__(self, x, y, text, obj_size:list, font_size) -> None:
        super(LevelObject, self).__init__()
        super().__init__()  
        self.margin = 4
        w, h = obj_size
        w = w -self.margin
        h = h -self.margin
        obj_size = (w, h)
        self.image = pygame.Surface(obj_size)  # assume the size of the object is 50*50
        self.image.fill(color_black)  # fill the object with grey color 
        self.rect = self.image.get_rect() 
        
        self.rect.topleft = (x+self.margin, y+self.margin) 
        self.text = str(text)
        self.font = pygame.font.SysFont('None', font_size)  # use default font and size
        self.update_text()  
  
    def update_text(self):  
        text = self.font.render(self.text, True, (color_white))  # render the text
        self.image.blit(text, (30, 30))  # display the text, offset by 5 pixels from the top left corner
  
    def collision(self, mouse_pos):  
        mouse_x, mouse_y = mouse_pos
        # judge if the mouse is in the rect 
        if self.rect.collidepoint(mouse_x, mouse_y):  
            return True  
        return False

# Define the game level interface class, used to select the game level
class GameLevelInterface(object):
    def __init__(self, **kwargs) -> None:
        self.top_title_font_size = 36 
        self.margin = 2
        self.win_size = kwargs.get('win_size')
        self.screen = kwargs.get('screen')
        self.user = kwargs.get('user')
        self.common_methond = kwargs.get('common_methond')
        self.return_main_text = kwargs.get('return_main_text')
        self.game_status_code = kwargs.get('game_status_code')
        self.levels_column = 5
        # Generate level buttons

        self.maze_min_level = 11
        self.maze_max_level = 43
        self.level_interval = 2
        self.total_maze_levels = (self.maze_max_level - self.maze_min_level) // self.level_interval + 1
        levels = kwargs.get('level')
        self.levels = []

        for one in range(0, levels // 5):
            start_level = one * self.levels_column + 1
            end_level = start_level + self.levels_column
            self.levels.append(list(range(start_level, end_level)))

        # Handle the remaining levels, if any
        remaining_levels = levels % 5
        if remaining_levels > 0:
            start_level = levels - remaining_levels + 1
            self.levels.append(list(range(start_level, levels + 1)))

        self.levels_objs = []
        self.all_sprites = pygame.sprite.Group()  # create a sprite group to manage all sprites
        self.first = True

    # When a level is selected, map it to the corresponding maze level
    def get_maze_level(self, selection_level):
        maze_level = self.maze_min_level + (selection_level - 1) * self.level_interval
        return min(maze_level, self.maze_max_level)

    # Query the current level of the user
    def query_db_level(self):
        with sqlite3.connect('user_data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT level FROM users WHERE username=?', (self.user,))
            level = cursor.fetchone()
            return level[0]

    # Update the level of the user in the database, if the current level is higher than the previous level of the user, update it
    def deal(self):
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for level_obj in self.levels_objs:
                        if level_obj.collision(event.pos):
                            selection_level = int(level_obj.text)
                            maze_level = self.get_maze_level(selection_level)
                            return [self.game_status_code[1], maze_level]

            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

    # Draw the game level interface, including the title, the level buttons, and the return button
    def draw(self):
        self.screen.fill(color_white)

        select_game_level_text_font = pygame.font.Font(None, self.top_title_font_size)
        select_game_level_text = select_game_level_text_font.render('Select Game Level', True, (color_black))
        text_title_rect = select_game_level_text.get_rect()
        text_title_rect.topleft = (self.margin, self.margin)
        self.screen.blit(select_game_level_text, text_title_rect)

        if self.first:
            level_text_font_size = self.top_title_font_size*2
            obj_topleft_x = self.margin*16
            obj_size = [(self.win_size[0] - obj_topleft_x*2)//self.levels_column,
                        (self.win_size[0] - obj_topleft_x*2)//self.levels_column]

            for outter_index, i in enumerate(self.levels):
                for index, j in enumerate(i):
                    self.levels_objs.append(LevelObject(obj_topleft_x + index *obj_size[0], 
                                                text_title_rect.bottom+self.margin + outter_index*obj_size[0],
                                                j, 
                                                obj_size,
                                                level_text_font_size)
                                    )
            self.all_sprites.add(self.levels_objs)
            self.first = False

    