import pygame, sys, sqlite3
from pygame.locals import *

pygame.init()
size = width,height = 645,970
bg = (0, 0, 0)
screen = pygame.display.set_mode(size)

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

username_input_rect = None
passowrd_input_rect = None
exit_login_rect = None
login_button_rect = None
username_input_active = False
password_input_active = False
username_text = ""
password_text = ""
margin = 2
top_title_font_size = 36
user_ps_len = 10

def draw_text_input(label, position):
    text_font = pygame.font.Font(None, 24)
    text = text_font.render(label, True, (color_black))
    text_rect = text.get_rect()
    text_rect.topleft = position
    screen.blit(text, text_rect)

    input_rect = pygame.Rect(position[0] + 110, position[1], 140, 32)
    input_rect.centery = text_rect.centery
    draw_rect = pygame.draw.rect(screen, (color_black), input_rect, 2)
    return draw_rect, text_rect

def draw_button(label, position, width, height):
    button_rect = pygame.Rect(position[0], position[1], width, height)
    if label == 'Login' or label == 'Register':
        text_font  = pygame.font.Font(None, 24) 
        pygame.draw.rect(screen, (color_grey), button_rect)
    else:
        text_font = pygame.font.Font(None, 24) 
    text = text_font.render(label, True, (color_black))
    text_rect = text.get_rect()
    text_rect.center = button_rect.center
    screen.blit(text, text_rect)
    return button_rect


# Login interface
def draw_login_interface(**kwargs):
    screen.fill(color_white)
    ps_error_msg, user_error_msg = kwargs.get('ps_error_msg'), kwargs.get('user_error_msg')
    is_register = kwargs.get('is_register', False)
    if is_register:
        login_label = 'Register'
    else:
        login_label = "Login"
    
    log_msg = kwargs.get('log_msg')
    

    # add title
    text_font = pygame.font.Font(None, top_title_font_size)
    text_title = text_font.render(login_label, True, (color_black))
    text_title_rect = text_title.get_rect()
    text_title_rect.topleft = (margin, margin)
    screen.blit(text_title, text_title_rect)

    global username_input_rect, passowrd_input_rect, login_button_rect, exit_login_rect
    # add username and password input box
    username_input_rect, username_rect = draw_text_input("Username:", (width / 2 - 100, 200))
    passowrd_input_rect, ps_rect = draw_text_input("Password:", (width / 2 - 100, 250))
    
    # exit login ui
    exit_button_width, exit_button_height = 100, 40
    return_main_text = text_font.render(u'Return Main', True, (color_black))
    exit_login_rect = return_main_text.get_rect()
    exit_login_rect.topleft = (width - exit_login_rect.width -margin, margin)
    screen.blit(return_main_text, exit_login_rect)

    # add login button
    login_button_rect = draw_button(login_label, (ps_rect.left, passowrd_input_rect.bottom+16), 
                             exit_button_width + username_input_rect.width +10, exit_button_height)
    
    text_font = pygame.font.Font(None, 24)
    error_color = (color_red)
    if ps_error_msg is not None:
        text = text_font.render(ps_error_msg, True, error_color)
        text_rect = text.get_rect()
        text_rect.topleft = (passowrd_input_rect.right+margin, passowrd_input_rect.top)
        screen.blit(text, text_rect)
    if user_error_msg is not None:
        text = text_font.render(user_error_msg, True, error_color)
        text_rect = text.get_rect()
        text_rect.topleft = (username_input_rect.right+margin, username_input_rect.top)
        screen.blit(text, text_rect)
    if log_msg is not None:
        text = text_font.render(log_msg, True, error_color)
        text_rect = text.get_rect()
        text_rect.center = (width//2, login_button_rect.bottom+text_rect.height//2)
        screen.blit(text, text_rect)

# Register interface
def draw_register_interface():
    screen.fill(color_white)
    
    # add title
    text_font = pygame.font.Font(None, 36)
    text_title = text_font.render(u'Register', True, (255, 255, 255))
    text_title_rect = text_title.get_rect()
    text_title_rect.center = (width / 2, 100)
    screen.blit(text_title, text_title_rect)

    # add username and password input box
    draw_text_input("Username:", (width / 2 - 100, 200))
    draw_text_input("Password:", (width / 2 - 100, 250))

    # add register button
    draw_button("Register", (width / 2 - 50, 320), 100, 40)

# Login interface
def handle_login_events(**kwargs):
    global username_input_active, password_input_active, \
            username_text,password_text, size, width, height, screen
    game_main_status = kwargs.get('game_main_status', 0)
    Gamestate_code:list = kwargs.get('Gamestate_code')
    size = width, height = kwargs.get('win_size')
    is_register = kwargs.get('is_register', False)
    screen = pygame.display.set_mode(size)

    is_exit = False
    ps_error_msg, user_error_msg = None, None
    log_msg = None
    while not is_exit:
        kwargs['ps_error_msg'] = ps_error_msg
        kwargs['user_error_msg'] = user_error_msg
        kwargs['log_msg'] = log_msg
        draw_login_interface(**kwargs)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    # mouse_pos = event.pos
                    # handle username input box
                    # if 200 <= mouse_pos[0] <= 340 and 200 <= mouse_pos[1] <= 232:
                    if username_input_rect.collidepoint(event.pos):
                        username_input_active = True
                        password_input_active = False
                    # handle password input box
                    # elif 200 <= mouse_pos[0] <= 340 and 250 <= mouse_pos[1] <= 282:
                    elif passowrd_input_rect.collidepoint(event.pos):
                        username_input_active = False
                        password_input_active = True 
                    # handle login button
                    elif login_button_rect.collidepoint(event.pos):
                        if is_register:
                            log_msg = register(username_text, password_text)
                        else:
                            log_msg = login(username_text, password_text)
                        if log_msg == True:
                            return Gamestate_code[0], username_text #game_level_interface
                    elif exit_login_rect.collidepoint(event.pos):
                        return game_main_status, None

            elif event.type == KEYDOWN:
                # handle keyboard events
                if username_input_active or password_input_active:
                    if event.key == K_RETURN:
                        # if press enter, login
                        if is_register:
                            log_msg = register(username_text, password_text)
                        else:
                            log_msg = login(username_text, password_text)
                        if log_msg == True:
                            return Gamestate_code[0], username_text #game_level_interface
                    elif event.key == K_BACKSPACE:
                        # if press backspace, delete the last character
                        if username_input_active:
                            username_text = username_text[:-1]
                        elif password_input_active:
                            password_text = password_text[:-1]
                    else:
                        # add the character to the input box
                        if username_input_active:
                            username_text += event.unicode
                        elif password_input_active:
                            password_text += event.unicode

        # display the input box
        # draw_text_input("Username: " + username_text, (width / 2 - 100, 200))
        # draw_text_input("Password: " + "*" * len(password_text), (width / 2 - 100, 250))
        user_error_msg, username_text = draw_input_text(username_input_rect, username_text, (width / 2 - 100, 200))
        ps_error_msg, password_text = draw_input_text(passowrd_input_rect, "*" * len(password_text), (width / 2 - 100, 250))

        # handle login button
        # draw_button("Login", (width / 2 - 50, 320), 100, 40)
        pygame.display.flip()
    # clock.tick(60)

# draw input text and return error message and label text 
def draw_input_text(rect_ui:pygame.Rect, label, position):
    error_msg = None
    text_font = pygame.font.Font(None, 24)
    if len(label) > user_ps_len:
        label = label[:10]
        error_msg = f'over {user_ps_len},only use previce{user_ps_len} '
    text = text_font.render(label, True, (color_black))
    text_rect = text.get_rect()
    text_rect.center = rect_ui.center
    screen.blit(text, text_rect)
    draw_rect = pygame.draw.rect(screen, (color_black), rect_ui, 2)
    return error_msg, label
    
# handle register events
def handle_register_events(**kwargs):
    return handle_login_events(**kwargs)

# login logic
def login(username, password):
    # Connect to SQLite database
    msg = None
    if username is None or username == '':
        return 'username is empty'
    if password is None or password == '':
        return 'password is empty'
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Check if the user exists and the password is correct
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user_data = cursor.fetchone()

    if user_data:
        msg = True
    else:
        msg = "Login failed. Invalid username or password."

    # Commit changes and close the database connection
    conn.commit()
    conn.close()
    return msg

# register logic
def register(username, password):
    msg = None
    if username is None or username == '':
        return 'username is empty'
    if password is None or password == '':
        return 'password is empty'
    # Connect to SQLite database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        msg = "Registration failed. Username already exists."
    else:
        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        msg = True

    # Commit changes and close the database connection
    conn.commit()
    conn.close()
    return msg

