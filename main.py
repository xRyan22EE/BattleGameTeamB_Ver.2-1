import os
import sys
from pathlib import Path

# Setup base directories
def setup_directories():
    # Get the directory containing the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define required directories relative to script location
    required_dirs = {
        'images': os.path.join(script_dir, 'images'),
        'sound': os.path.join(script_dir, 'sound'),
        'assets': os.path.join(script_dir, 'images', 'assets'),
        'ships': os.path.join(script_dir, 'images', 'ships'),
        'tokens': os.path.join(script_dir, 'images', 'tokens'),
        'buttons': os.path.join(script_dir, 'images', 'Button_Itch_Pack')
    }
    
    # Create directories if they don't exist
    for dir_path in required_dirs.values():
        os.makedirs(dir_path, exist_ok=True)
    
    return required_dirs

# Setup directories before imports
DIRS = setup_directories()

from grid import CreateGameGrid
from game_utils import LoadImage
from Buttons import Button, box_Button
from Display_Turns import display_turn
from search_system import search_hit
from BG import moving_background
from Ai import *
from button import Slider
from button import Button as Button_menue

# Import modules
import pygame
import random
import copy
import os
import time
import sys


pygame.init()

# Update paths to use DIRS
SCREEN = pygame.display.set_mode((1260, 950))
pygame.display.set_caption("Battle Ship Demo")
grid_size_menu = 10
volume_value = 0.1

# Use os.path.join for file paths
icon = pygame.image.load(os.path.join(DIRS['assets'], 'ShipGame.png'))
pygame.display.set_icon(icon)

BG = pygame.image.load(os.path.join(DIRS['assets'], 'Background.png')).convert_alpha()
BG = pygame.transform.scale(BG, (1260, 950))
BG_rect = BG.get_rect(center=(630, 475))

# Load music with error handling
try:
    pygame.mixer.music.load(os.path.join(DIRS['sound'], 'Metal Gear Solid Main Theme mp3.mp3'))
    pygame.mixer.music.set_volume(volume_value)
    pygame.mixer.music.play(-1)
except pygame.error:
    print("Warning: Could not load background music")

volume_slider = Slider((630, 775), (500, 25), pygame.mixer.music.get_volume(), 0, 100)

def get_font(size):  # Returns Press-Start-2P in the desired size
    font_path = os.path.join(DIRS['assets'], 'font.ttf')
    try:
        return pygame.font.Font(font_path, size)
    except OSError:
        print(f"Warning: Could not load font at {font_path}")
        return pygame.font.SysFont("Arial", size)

def play():
    game()

def options():
    global volume_value
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        
        SCREEN.blit(BG, (BG_rect.x, BG_rect.y))


        
        OPTIONS_TEXT = get_font(100).render("OPTIONS", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(630, 150))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        VOLUME_TEXT = get_font(50).render("Volume", True, "white")
        VOLUME_RECT = VOLUME_TEXT.get_rect(center=(630, 475 + 210))
        SCREEN.blit(VOLUME_TEXT, VOLUME_RECT)

        OPTIONS_BACK = Button_menue(image=None, pos=(630, 475 + 380), text_input="BACK", font=get_font(50), base_color="white", hovering_color="Green")
        FULL_SCREEN = Button_menue(image=None, pos=(630, 475), text_input="Full Screen", font=get_font(50), base_color="white", hovering_color="Green")
        DEFCULT = Button_menue(image=None, pos=(630, 475 + 120), text_input="Difficulty", font=get_font(50), base_color="white", hovering_color="Green")
        
        for button in [OPTIONS_BACK, FULL_SCREEN, DEFCULT]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)




        if volume_slider.container_rect.collidepoint(OPTIONS_MOUSE_POS):
            if pygame.mouse.get_pressed()[0]:
                volume_slider.hovered = True
                volume_slider.move_slider(OPTIONS_MOUSE_POS)
                volume_slider.display_value(SCREEN)
                pygame.mixer.music.unpause()
                pygame.mixer.music.set_volume(volume_slider.get_value() / 100)
        else:
            volume_slider.hovered = False
            
        volume_slider.render(SCREEN)
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if FULL_SCREEN.checkForInput(OPTIONS_MOUSE_POS):
                    if SCREEN.get_flags() & pygame.FULLSCREEN:
                        pygame.display.set_mode((1260, 950))
                    else:
                        pygame.display.set_mode((1260, 950), pygame.FULLSCREEN)


                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if DEFCULT.checkForInput(OPTIONS_MOUSE_POS):
                    defcult()

        pygame.display.update()

def defcult():
    global grid_size_menu
    while True:
        SCREEN.blit(BG, (BG_rect.x, BG_rect.y))
        DEFCULT_MOUSE_POS = pygame.mouse.get_pos()

        DEFCULT_TEXT = get_font(100).render("DIFFICULTY", True, "#b68f40")
        DEFCULT_RECT = DEFCULT_TEXT.get_rect(center=(630, 150))
        SCREEN.blit(DEFCULT_TEXT, DEFCULT_RECT)

        EASY_BUTTON = Button_menue(image=None, pos=(630, 475), text_input="EASY", font=get_font(75), base_color="white", hovering_color="green")
        MEDIUM_BUTTON = Button_menue(image=None, pos=(630, 475 + 120), text_input="MEDIUM", font=get_font(75), base_color="white", hovering_color="green")
        HARD_BUTTON = Button_menue(image=None, pos=(630, 475 + 240), text_input="HARD", font=get_font(75), base_color="white", hovering_color="green")
        BACK_BUTTON = Button_menue(image=None, pos=(630, 475 + 360), text_input="BACK", font=get_font(75), base_color="white", hovering_color="green")
        if grid_size_menu == 10:
            EASY_BUTTON.base_color = ("green")
        elif grid_size_menu == 12:
            MEDIUM_BUTTON.base_color = ("green")
        elif grid_size_menu == 15:
            HARD_BUTTON.base_color = ("green")

        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON, BACK_BUTTON]:
            button.changeColor(DEFCULT_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(DEFCULT_MOUSE_POS):
                    grid_size_menu = 10
                if MEDIUM_BUTTON.checkForInput(DEFCULT_MOUSE_POS):
                    grid_size_menu = 12
                if HARD_BUTTON.checkForInput(DEFCULT_MOUSE_POS):
                    grid_size_menu = 15
                if BACK_BUTTON.checkForInput(DEFCULT_MOUSE_POS):
                    options()
        pygame.display.update()

def instructions():
    while True:
        SCREEN.blit(BG, (BG_rect.x, BG_rect.y))
        INSTRACTION_MOUSE_POS = pygame.mouse.get_pos()

        INSTRACTION_TEXT = get_font(50).render("INSTRUCTIONS", True, "#b68f40")  # Reduced size from 100 to 75
        
        # New instructions text
        instructions_text = [
            "How to Play:",
            "",
            "Placing Ships:",
            "- Drag and drop ships on to your grid or use the Random button",
            "- Ships cannot overlap or go outside the grid",
            "",
            "Gameplay:",
            "- Take turns attacking by clicking on opponent's grid",
            "- Fire marker = hit, Blue marker = miss",
            "- AI plays automatically after your turn",
            "",
            "Winning:",
            "- Destroy all enemy ships to win",
            "- Game ends when your ships are destroyed",
            "",
            "Tips:",
            "- For more challenge, change the grid size in settings",
            "- Easy: 10x10:",
            "- Medium: 12x12:",
            "- Hard: 15x15:"
        ]

        INSTRACTIONS = [get_font(20).render(line, True, "white") for line in instructions_text]  # Reduced size from 25 to 20

        INSTRACTION_RECT = INSTRACTION_TEXT.get_rect(center=(630, 100))  # Moved up from 150 to 100
        SCREEN.blit(INSTRACTION_TEXT, INSTRACTION_RECT)

        y_offset = 200  # Adjusted starting position from 300 to 250
        for line in INSTRACTIONS:
            line_rect = line.get_rect(center=(630, y_offset))
            SCREEN.blit(line, line_rect)
            y_offset += 30  # Reduced spacing from 35 to 30

        INSTRACTION_BACK = Button_menue(image=None, pos=(640, 850), text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        INSTRACTION_BACK.changeColor(INSTRACTION_MOUSE_POS)
        INSTRACTION_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if INSTRACTION_BACK.checkForInput(INSTRACTION_MOUSE_POS):
                    main_menu()
                    
        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (BG_rect.x, BG_rect.y))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(630, 150))
        INSTRACTION_IMG = pygame.image.load(os.path.join(DIRS['assets'], 'Options Rect.png')).convert_alpha()
        INSTRACTION_IMG = pygame.transform.scale(INSTRACTION_IMG, (950, 110))
        

        PLAY_BUTTON = Button_menue(image=pygame.image.load(os.path.join(DIRS['assets'], 'Play Rect.png')), pos=(630, 475), text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="green")
        OPTIONS_BUTTON = Button_menue(image=pygame.image.load(os.path.join(DIRS['assets'], 'Options Rect.png')), pos=(630, 475 + 120), text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="green")
        QUIT_BUTTON = Button_menue(image=pygame.image.load(os.path.join(DIRS['assets'], 'Quit Rect.png')), pos=(630, 475 + 360), text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="green")
        INSTRACTION = button = Button_menue(image=INSTRACTION_IMG, pos=(630, 475 + 240), text_input="INSTRUCTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="green")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, INSTRACTION]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if INSTRACTION.checkForInput(MENU_MOUSE_POS):
                        instructions()
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()


def game():
    global SCREEN, game_paused, scroll, setting_button, game_started, randomize_button, start_button, fullscreen, ai_img, player_img, ai_img_rect, player_img_rect, ScreenWidth, ScreenHight, grid_size, resetGameGrid, game_over, ScreenXcenter, ScreenYcenter, BG_border_old, BG_border, BG_width, BG_tiles, BG_img, white, black, red, green, blue, orange, colors, miss_img, hit_img, sunk_img, old_miss_img, old_hit_img, old_sunk_img, pGameGrid, cGameGrid, pGameLogic, cGameLogic, Playerfleet, Computerfleet, raws, cols, CellSize, pGameGrid, pGameLogic, cGameGrid, cGameLogic, copy_grids, Players_fleet, Player1Health, Player2Health, game_over, yCooForShots, xCooForShots, start_img, exit_img, setting_img, randomize_img, settings_panel, settings_panel_rect, clock, GameScreen, ai_values, ai_turn, number_of_sunk_ship_ai, number_of_sunk_ship_player, gameover_sound, player_lose_sound, player_win_sound, game_started, game_paused, ai_vs_player, randomized, play_gameover_once, ai_values, ai_turn, number_of_sunk_ship_ai, number_of_sunk_ship_player, gameover_sound, player_lose_sound, player_win_sound, game_started, game_paused, ai_vs_player, randomized, play_gameover_once, miss_sound, hit_sound, sunk_sound, BG, BG_rect, volume_slider, value

    # - - - - - - - - - - - - - - - - - - Initialization - - - - - - - - - - - - - - - - - -
    # set main directory to the whole project's file
    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(assets_dir)

    # module Initialization
    pygame.init()
    clock = pygame.time.Clock()

    # game variables
    game_started = False  # variable to check if the game has started
    game_paused = False  # variable to check if the game is paused
    resetGameGrid = True
    game_over = False
    ai_vs_player = True
    randomized = True
    play_gameover_once = True

    # Game Settings and Variables
    ScreenWidth = 1260
    ScreenHight = 950

    # Set colors (R,G,B)
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    orange = (245, 145, 30)

    # pygame display Initialization
    GameScreen = SCREEN

    # display variable for the game screen
    ScreenXcenter = 630  # get the center of the screen width
    ScreenYcenter = 475 # get the center of the screen height

    # set the title of the window
    pygame.display.set_caption("Battle Ship Demo")

    # - - - - - - - - - - - -  - - - Initialize Game's Grids - - - - - - - - - - - - - - -
    # Set grid size based on chosen difficulty (Get it from Main Menu)
    grid_size = grid_size_menu

    # Set grid size based on user input
    def set_grid_size(new_rows: int, new_cols: int) -> None:
        # function to set grid size and dynamically adjust cell size
        global rows, cols, CellSize, pGameGrid, pGameLogic, cGameGrid, cGameLogic
        rows = new_rows
        cols = new_cols

        # divide ScreenHeight by 2 to leave space for both grids and divide by rows to get the cell size for the grid
        CellSize = min(ScreenWidth // cols, ScreenHight // (2 * rows))
        # create game grid for player and computer grid with the new rows, cols and cell size
        pGameGrid = CreateGameGrid(rows, cols, CellSize, (50, 50))
        cGameGrid = CreateGameGrid(rows, cols, CellSize, (((ScreenWidth - 50) - (cols * CellSize)), 50))

    # set the grid size for the game (rows, cols)
    set_grid_size(grid_size, grid_size)

    # Set first shot out of boundaries till the user input
    yCooForShots = grid_size + 1
    xCooForShots = grid_size + 1

    #  - - - - - - - - - - - - - - - Game Lists/Dictionaries - - - - - - - - - - - - - - -
    # Initialize copy of players grids, where copy_grids[0] is a list for player 1, and copy_grids[1] is a list for player 2
    copy_grids = [[], []]

    # Players_fleet  = Player Fleet Dictionary     key: [name, image path, position, size, health]
    Players_fleet = {
        "carrier": ["carrier", os.path.join(DIRS['ships'], 'carrier', 'carrier.png'), (50, 600), 5],
        "battleship": ["battleship", os.path.join(DIRS['ships'], 'battleship', 'battleship.png'), (125, 600), 4],
        "cruiser": ["cruiser", os.path.join(DIRS['ships'], 'cruiser', 'cruiser.png'), (200, 600), 4],
        "destroyer": ["destroyer", os.path.join(DIRS['ships'], 'destroyer', 'destroyer.png'), (275, 600), 3],
        "submarine": ["submarine", os.path.join(DIRS['ships'], 'submarine', 'submarine.png'), (350, 600), 3],
        "patrol boat": ["patrol boat", os.path.join(DIRS['ships'], 'patrol boat', 'patrol boat.png'), (425, 600), 2],
        "rescue ship": ["rescue ship", os.path.join(DIRS['ships'], 'rescue ship', 'rescue ship.png'), (500, 600), 2]
    }

    # Set Players Ship's Health, where each key represents the firs two letters of the ship's name
    Player1Health = {
        "ca": 5, "ba": 4, "cr": 4, "de": 3, "su": 3, "pa": 2, "re": 2}

    Player2Health = {
        "ca": 5, "ba": 4, "cr": 4, "de": 3, "su": 3, "pa": 2, "re": 2}

    # Set AI values
    ai_values = {'shots_taken': [], 'unknown_cells': [], 'hit_cells': [], 'sunken_cells': [], 'last_hit': '', 'first_hit': False, 'tries': 0 }
    ai_turn = []

    # Set number of sunken ships for each player
    number_of_sunk_ship_ai = 0
    number_of_sunk_ship_player = 0

    #  - - - - - - - - - - - - loading game sound and Image - - - - - - - - - - - - - -
    # background image path and variables
    BG_border_old = pygame.image.load(os.path.join(DIRS['images'], 'BG', 'radar_border.png')).convert_alpha()
    BG_border = pygame.transform.scale(BG_border_old, (ScreenWidth, ScreenHight))
    # Scroll background by using moving_background function for the file BG.py
    BG_width, BG_tiles, BG_img = moving_background(os.path.join(DIRS['images'], 'BG', 'download.png'), ScreenWidth, ScreenHight)

    # Define scrolling background variables
    scroll = 0
    tiles = 2  # Number of tiles to cover the screen width

    # Buttons layout
    randomize_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Random', 'Random_1.png'))
    start_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Start', 'Start1.png')).convert_alpha()
    setting_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Settings', 'Settings1.png')).convert_alpha()
    ai_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Turns', 'Ai.png'))
    player_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Turns', 'Player.png'))

    ai_img = pygame.transform.scale(ai_img, (150, 150))
    player_img = pygame.transform.scale(player_img, (150, 150))
    ai_img_rect = ai_img.get_rect(center=(ScreenXcenter, ScreenYcenter))
    player_img_rect = player_img.get_rect(center=(ScreenXcenter, ScreenYcenter))

    # Hits images
    old_miss_img = pygame.image.load(os.path.join(DIRS['tokens'], 'bluetoken.png')).convert_alpha()
    miss_img = pygame.transform.scale(old_miss_img, (CellSize, CellSize))

    old_hit_img = pygame.image.load(os.path.join(DIRS['tokens'], 'fire.png')).convert_alpha()
    hit_img = pygame.transform.scale(old_hit_img, (CellSize, CellSize))

    old_sunk_img = pygame.image.load(os.path.join(DIRS['tokens'], 'explosion_sunk.png')).convert_alpha()
    sunk_img = pygame.transform.scale(old_sunk_img, (CellSize, CellSize))

    # Background theme


    # shots sounds
    miss_sound = pygame.mixer.Sound(os.path.join(DIRS['sound'], 'miss.mp3'))
    miss_sound.set_volume(0.5)
    hit_sound = pygame.mixer.Sound(os.path.join(DIRS['sound'], 'hit.mp3'))
    hit_sound.set_volume(0.5)
    sunk_sound = pygame.mixer.Sound(os.path.join(DIRS['sound'], 'sunk.mp3'))
    sunk_sound.set_volume(0.5)

    # Game over sound effect
    gameover_sound = pygame.mixer.Sound(os.path.join(DIRS['sound'], 'gameover.mp3'))
    gameover_sound.set_volume(0.5)

    player_lose_sound = pygame.mixer.Sound(os.path.join(DIRS['sound'], 'player_lose.mp3'))
    player_lose_sound.set_volume(0.5)

    player_win_sound = pygame.mixer.Sound(os.path.join(DIRS['sound'], 'player_win.mp3'))
    player_win_sound.set_volume(0.5)

    # - - - - - - - - - - - - - - Buttons - - - - - - - - - - - - - -
    # Button instance for start and exit button
    start_button = Button(ScreenXcenter, ScreenYcenter, start_img, ScreenHight, ScreenWidth)
    randomize_button = Button(ScreenXcenter, ScreenYcenter + ScreenHight // 15, randomize_img, ScreenHight, ScreenWidth)
    setting_button = Button(ScreenXcenter, ScreenYcenter + ScreenHight // 15, setting_img, ScreenHight, ScreenWidth)

    # Create buttons for settings panel
    settings_panel = pygame.Surface((400, 500))
    settings_panel.fill((50, 50, 50))  # Dark gray background
    settings_panel_rect = settings_panel.get_rect(center=(ScreenXcenter, ScreenYcenter))  # Center the panel on the screen

    # - - - - - - - - Game Assets and Objects - - - - - - - - -
    class ship:
        # Class variable to store all created instances
        instances = []

        def __init__(self, name: str, img: str, pos: tuple, size: tuple):
            self.name = name

            # Set the start position of the ship to the position passed in the constructor. This is the position the ship will return to if it is not placed in the grid.
            self.start_pos = pos

            # Load the Vertical Image.
            self.vimg = LoadImage(img, size)
            self.vimgwidth = self.vimg.get_width()
            self.vimgheight = self.vimg.get_height()
            self.vimgrect = self.vimg.get_rect()
            self.vimgrect.topleft = pos

            # Load the Horizontal Image.
            self.himg = pygame.transform.rotate(self.vimg, -90)
            self.himgwidth = self.himg.get_width()
            self.himgheight = self.himg.get_height()
            self.himgrect = self.himg.get_rect()
            self.himgrect.topleft = pos

            # ship selection
            self.active = False

            # Image and rectangle
            self.image = self.vimg
            self.rect = self.vimgrect
            self.rotation = False

            # Append the current instance to the class variable instances
            ship.instances.append(self)

        def resize_ship(self, cell_count):
            # Update the size based on the cell count and current CellSize
            adjusted_size = (CellSize, cell_count * CellSize) if not self.rotation else (cell_count * CellSize, CellSize)
            self.vimg = pygame.transform.scale(self.vimg, adjusted_size)
            self.himg = pygame.transform.rotate(self.vimg, -90)  # Rotate for horizontal
            self.rect = self.vimg.get_rect()
            self.himgrect = self.himg.get_rect()
            self.rect.topleft = self.start_pos  # Reset to starting position if needed

        def set_grid_size(new_rows: int, new_cols: int) -> None:
            global rows, cols, CellSize, pGameGrid, pGameLogic, cGameGrid, cGameLogic
            rows = new_rows
            cols = new_cols

            # Calculate CellSize based on grid dimensions
            CellSize = min(ScreenWidth // cols, ScreenHight // (2 * rows))
            # Re-create the player and computer grids
            pGameGrid = CreateGameGrid(rows, cols, CellSize, (50, 50))
            cGameGrid = CreateGameGrid(rows, cols, CellSize, (((ScreenWidth - 50) - (cols * CellSize)), 50))

            # Resize each ship according to the new CellSize
            for ship in Playerfleet + Computerfleet:
                ship.resize_ship(Players_fleet[ship.name][3])  # Pass in the cell count for each ship

        def selectshipandmove(self) -> None:
            if game_started or game_paused:
                return

            while self.active:
                self.rect.center = pygame.mouse.get_pos()
                UpdateGameScreen(GameScreen)
                time.sleep(0.012)

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if not self.check_for_collision(Playerfleet):
                            if event.button == 1:
                                if self.CheckinGrid(pGameGrid):
                                    self.snap_to_grid(pGameGrid)
                                    self.himgrect.center = self.vimgrect.center = self.rect.center
                                    self.active = False
                                else:
                                    self.return_to_start()
                                    self.active = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        # Rotate the ship if the space key is pressed
                        self.rotate_ship()

        def rotate_ship(self):
            # Toggle the rotation state
            self.rotation = not self.rotation

            # Update the image and rectangle based on the new orientation
            if self.rotation:
                self.image = self.himg
                self.rect = self.himgrect
            else:
                self.image = self.vimg
                self.rect = self.vimgrect
            self.rect.center = pygame.mouse.get_pos()

        def CheckinGrid(self, grid: list) -> bool:
            for row in grid:
                for col in row:
                    cell_rect = pygame.Rect(col[0], col[1], CellSize, CellSize)
                    if self.rect.colliderect(cell_rect):
                        return True
            return False

        def return_to_start(self) -> None:
            self.rotation = False
            self.image = self.vimg
            self.rect = self.vimgrect
            self.rect.topleft = self.start_pos
            self.vimgrect.topleft = self.start_pos
            self.himgrect.topleft = self.start_pos
            self.active = False

        def snap_to_grid(self, grid: list):
            if self.rotation:
                cells_required_x = self.rect.width // CellSize
                cells_required_y = 1
            else:
                cells_required_x = 1
                cells_required_y = self.rect.height // CellSize

            current_top_left = self.rect.topleft
            closest_cell_top_left = None
            min_distance = float("inf")

            if self.CheckinGrid(pGameGrid):
                for row in grid:
                    for col in row:
                        cell_top_left_x = col[0]
                        cell_top_left_y = col[1]
                        distance = ((current_top_left[0] - cell_top_left_x) ** 2 +
                                    (current_top_left[1] - cell_top_left_y) ** 2) ** 0.5

                        if distance < min_distance:
                            min_distance = distance
                            closest_cell_top_left = (cell_top_left_x, cell_top_left_y)

                if closest_cell_top_left:
                    snapped_x = closest_cell_top_left[0]
                    snapped_y = closest_cell_top_left[1]

                    border = 530
                    if self.rotation:
                        if snapped_x + cells_required_x * CellSize > border:
                            snapped_x = border - cells_required_x * CellSize
                    else:
                        if snapped_y + cells_required_y * CellSize > border:
                            snapped_y = border - cells_required_y * CellSize

                    if self.rotation:
                        if snapped_x + (cells_required_x * CellSize) <= ScreenWidth and snapped_y <= ScreenHight:
                            self.rect.topleft = closest_cell_top_left
                            self.rect.centerx = snapped_x + (cells_required_x * CellSize) // 2
                            self.rect.centery = snapped_y + (cells_required_y * CellSize) // 2
                        else:
                            self.return_to_start()
                    else:
                        if snapped_y + (cells_required_y * CellSize) <= ScreenHight:
                            self.rect.topleft = closest_cell_top_left
                            self.rect.centerx = snapped_x + (cells_required_x * CellSize) // 2
                            self.rect.centery = snapped_y + (cells_required_y * CellSize) // 2
                        else:
                            self.return_to_start()

        def computer_snap_to_grid(self, grid: list):
            if self.rotation:  # Horizontal

                # Calculate the number of cells required to fit the ship
                cells_required_x = self.rect.width // CellSize

                # The ship is always 1 cell tall when horizontal
                cells_required_y = 1

            else:  # Vertical
                # The ship is always 1 cell wide when vertical
                cells_required_x = 1

                # Calculate the number of cells required to fit the ship
                cells_required_y = self.rect.height // CellSize

            # Get the top-left position of the ship
            current_top_left = self.rect.topleft

            # Initialize variables to store the closest cell's top-left position and the minimum distance
            closest_cell_top_left = None

            # Set the minimum distance to infinity to ensure the first cell is selected
            min_distance = float("inf")

            # Iterate through the grid to find the closest cell to the ship
            for row in grid:
                for col in row:
                    # Get the top-left position of the current cell
                    cell_top_left_x = col[0]
                    cell_top_left_y = col[1]

                    # Calculate the distance between the ship and the current cell
                    distance = ((current_top_left[0] - cell_top_left_x) ** 2 + (
                            current_top_left[1] - cell_top_left_y) ** 2) ** 0.5
                    # Pythagorean theorem (a^2 + b^2 = c^2) to calculate the distance between two points in 2D space (x, y)

                    # Check if the current cell is closer to the ship than the previous closest cell
                    if distance < min_distance:
                        # Update the minimum distance and the closest cell's top-left position
                        min_distance = distance

                        # Set the closest cell's top-left position to the current cell's top-left position
                        closest_cell_top_left = (cell_top_left_x, cell_top_left_y)

            # Check if closest cell was found
            if closest_cell_top_left:
                # Get the x and y coordinates of the closest cell's top-left position
                snapped_x = closest_cell_top_left[0]
                # Get the y coordinate of the closest cell's top-left position
                snapped_y = closest_cell_top_left[1]

                # Ensure the ship does not go out of the grid boundaries
                if self.rotation:  # Horizontal
                    # Check if the ship is within the grid boundaries when horizontal and snap to the closest cell if it is
                    if snapped_x + cells_required_x * CellSize > ScreenWidth:
                        snapped_x = ScreenWidth - cells_required_x * CellSize
                else:  # Vertical
                    # Check if the ship is within the grid boundaries when vertical and snap to the closest cell if it is
                    if snapped_y + cells_required_y * CellSize > ScreenHight:
                        snapped_y = ScreenHight - cells_required_y * CellSize

                if self.rotation:  # Horizontal
                    # Snap the ship to the closest cell if it is within the grid boundaries when horizontal
                    if snapped_x + (cells_required_x * CellSize) <= ScreenWidth and snapped_y <= ScreenHight:
                        self.rect.topleft = closest_cell_top_left
                        self.rect.centerx = snapped_x + (cells_required_x * CellSize) // 2
                        self.rect.centery = snapped_y + (cells_required_y * CellSize) // 2
                    else:  # Return the ship to the start position if it is out of bounds
                        self.return_to_start()

                else:  # Vertical
                    # Snap the ship to the closest cell if it is within the grid boundaries when vertical
                    if snapped_y + (
                            cells_required_y * CellSize) <= ScreenHight:  # Check if the ship is within the grid boundaries

                        # Snap the ship to the closest cell if it is within the grid boundaries when vertical
                        self.rect.topleft = closest_cell_top_left

                        # Center the ship in the cell by setting the x and y coordinates to the center of the cell
                        self.rect.centerx = snapped_x + (cells_required_x * CellSize) // 2
                        self.rect.centery = snapped_y + (cells_required_y * CellSize) // 2
                    else:  # Return the ship to the start position if it is out of bounds
                        self.return_to_start()  # Return the ship to the start position if it is out of bounds

        def check_for_collision(self, other_ships: list) -> bool:
            CopyOfShip = other_ships.copy()
            CopyOfShip.remove(self)
            for ship in CopyOfShip:
                if self.rect.colliderect(ship.rect):
                    return True
            return False

        def draw(self, window: pygame.Surface) -> None:
            window.blit(self.image, self.rect)

            # pygame.draw.rect(window, red, self.rect, 1)  # Debugging: red rectangle around the ship

        def is_placed_in_grid(self) -> bool:
            # Check if the ship is placed in the grid and not active

            # Return True if the ship is placed in the grid and not active, otherwise return False
            return self.CheckinGrid(pGameGrid) and not self.active

        # Debugging methods
        def __str__(self):
            return f"{self.name}: {self.rect.center} || {self.rect} || {self.vimg} || {self.himg} "

        @classmethod
        def view_all_instances(cls):
            for ships in cls.instances:
                print(ships)


    # - - - - - - - - Ships Related Functions - - - - - - - -
    # Create fleet based on players fleet dictionary
    def createfleet() -> list:
        fleet = []
        for name, (img_name, img_path, pos, cell_count) in Players_fleet.items():
            # Calculate the ship size in pixels based on CellSize and cell count
            if name != "patrol boat" and name != "rescue ship":
                adjusted_size = (CellSize, cell_count * CellSize)
            else:
                adjusted_size = (CellSize * 0.65, CellSize * cell_count)
            fleet.append(ship(name, img_path, pos, adjusted_size))
        return fleet

    def randomized_computer_ships(shiplist: list, gamegrid: list) -> None:
        for ship in shiplist:
            placed = False
            while not placed:
                # Reset ship's position
                ship.return_to_start()

                # Randomly select rotation and apply it
                rotate_ship = random.choice([True, False])
                if rotate_ship:
                    ship.rotate_ship()  # Rotate to horizontal if True
                else:
                    ship.rotation = False  # Keep vertical

                # Get the maximum position based on grid size and ship size to avoid going out of bounds
                max_x = len(gamegrid[0]) - (ship.rect.width // CellSize if ship.rotation else 1)
                max_y = len(gamegrid) - (1 if ship.rotation else ship.rect.height // CellSize)

                # Randomly select a starting cell within the allowed bounds
                start_x = random.randint(0, max_x)
                start_y = random.randint(0, max_y)

                # Calculate the top-left position in pixels for the grid
                ship.rect.topleft = (gamegrid[start_y][start_x][0], gamegrid[start_y][start_x][1])

                # Check if this position collides with other ships in the fleet
                if not ship.check_for_collision(shiplist):
                    # Snap to grid if valid, and mark as placed
                    ship.computer_snap_to_grid(gamegrid)
                    placed = True

    # Check if all ships are placed in the grid
    def all_ships_placed() -> bool:
        # Return True if all ships are placed in the grid, otherwise return False
        return all(ship.is_placed_in_grid() for ship in Playerfleet)

    # Make last ship taken the first priority
    def sortfleet(ship, shiplist: list) -> None:
        # function to sort ships in the list to the top of the list when selected to show on top of other ships
        shiplist.remove(ship)
        shiplist.append(ship)

    # function to handle ship selection
    def handle_ship_selection() -> None:
        # for loop to iterate through the player fleet
        for i in Playerfleet:

            # check if the mouse position is within the rectangle of the ship
            if i.rect.collidepoint(pygame.mouse.get_pos()):
                # set the ship to active
                i.active = True

                # sort the ship to the top of the list to show on top of other ships
                sortfleet(i, Playerfleet)

                # move the ship to the mouse position and update the game screen
                i.selectshipandmove()

    # - - - - - - - - Game Utility Functions - - - - - - - - -
    
    def instructions_Game(): # Instructions for the game play and how to play
        instructions_active = True
        original_screen = GameScreen.copy()  # Save the current game state
        
        while instructions_active:
            INSTRACTION_MOUSE_POS = pygame.mouse.get_pos()

            GameScreen.blit(BG, (BG_rect.x, BG_rect.y))

            INSTRACTION_TEXT = get_font(50).render("INSTRUCTIONS", True, "#b68f40")
            
            # New instructions text
            instructions_text = [
                "How to Play:",
                "",
                "Placing Ships:",
                "- Drag and drop ships on to your grid or use the Random button",
                "- Ships cannot overlap or go outside the grid",
                "",
                "Gameplay:",
                "- Take turns attacking by clicking on opponent's grid",
                "- Fire marker = hit, Blue marker = miss",
                "- AI plays automatically after your turn",
                "",
                "Winning:",
                "- Destroy all enemy ships to win",
                "- Game ends when your ships are destroyed",
                "",
                "Tips:",
                "- For more challenge, change the grid size in settings",
                "- Easy: 10x10:",
                "- Medium: 12x12:",
                "- Hard: 15x15:"
            ]

            INSTRACTIONS = [get_font(20).render(line, True, "white") for line in instructions_text]  # Reduced size from 25 to 20

            INSTRACTION_RECT = INSTRACTION_TEXT.get_rect(center=(630, 100))  # Moved up from 150 to 100
            GameScreen.blit(INSTRACTION_TEXT, INSTRACTION_RECT)

            y_offset = 200  # Adjusted starting position from 300 to 250
            for line in INSTRACTIONS:
                line_rect = line.get_rect(center=(630, y_offset))
                GameScreen.blit(line, line_rect)
                y_offset += 30  # Reduced spacing from 35 to 30

            INSTRACTION_BACK = Button_menue(image=None, pos=(640, 850), text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

            INSTRACTION_BACK.changeColor(INSTRACTION_MOUSE_POS)
            INSTRACTION_BACK.update(GameScreen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if INSTRACTION_BACK.checkForInput(INSTRACTION_MOUSE_POS):
                        instructions_active = False
                        
            pygame.display.update()

        GameScreen.blit(original_screen, (0, 0))  # Restore the game state
        pygame.display.update()

    # Make a copy of players grids to calculate hits
    def copyGrids():
        # Set start of game values

        # Player 1 values
        player1Grid = copy.deepcopy(copy_grids[0])
        player1_reference = copy.deepcopy(copy_grids[0])
        player1_fleet = copy.deepcopy(Player2Health)
        # Randomise players turns
        player1Turn = True

        # Player 2 values
        player2Grid = copy.deepcopy(copy_grids[1])
        player2_reference = copy.deepcopy(copy_grids[1])
        player2_fleet = copy.deepcopy(Player2Health)
        # Set player 2 turn as the opposite of player 1
        player2Turn = not player1Turn

        # Set lists for each player
        player1_values = {'player1Grid': player1Grid, 'player1_reference': player1_reference,
                        'player1_fleet': player1_fleet, 'player1Turn': player1Turn, 'last_hit': (9,9)}
        player2_values = {'player2Grid': player2Grid, 'player2_reference': player2_reference,
                        'player2_fleet': player2_fleet, 'player2Turn': player2Turn, 'last_hit': (8,8)}

        ai_turn = ai_thinking(grid_size, ai_values, player1_values)

        return player1_values, player2_values, ai_turn

    # Draw shots indicators
    def draw_shots(window, player1_values, player2_values):
        # Draw Player 1 grid hits
        for row in range(len(player1_values['player1Grid'])):
            for col in range(len(player1_values['player1Grid'][row])):
                xCooForShots = col
                yCooForShots = row
                try: # Use try & except to not draw on ships or empty cells
                    if player1_values['player1Grid'][row][col] == 'M':
                        window.blit(miss_img, (pGameGrid[yCooForShots][xCooForShots][0],pGameGrid[yCooForShots][xCooForShots][1]))
                    if player1_values['player1Grid'][row][col] == 'H':
                        window.blit(hit_img, (pGameGrid[yCooForShots][xCooForShots][0],pGameGrid[yCooForShots][xCooForShots][1]))
                    if player1_values['player1Grid'][row][col] == 'S':
                        window.blit(sunk_img,
                                    (pGameGrid[yCooForShots][xCooForShots][0], pGameGrid[yCooForShots][xCooForShots][1]))
                except:
                    pass

        # Draw Player 2 grid hits
        for row in range(len(player2_values['player2Grid'])):
            for col in range(len(player2_values['player2Grid'][row])):
                xCooForShots = col
                yCooForShots = row
                try: # Use try & except to not draw on ships or empty cells
                    if player2_values['player2Grid'][row][col] == 'M':
                        window.blit(miss_img, (cGameGrid[yCooForShots][xCooForShots][0],cGameGrid[yCooForShots][xCooForShots][1]))
                    if player2_values['player2Grid'][row][col] == 'H':
                        window.blit(hit_img, (cGameGrid[yCooForShots][xCooForShots][0],cGameGrid[yCooForShots][xCooForShots][1]))
                    if player2_values['player2Grid'][row][col] == 'S':
                        window.blit(sunk_img,
                                    (cGameGrid[yCooForShots][xCooForShots][0], cGameGrid[yCooForShots][xCooForShots][1]))
                except:
                    pass

    # Draw sunken ships
    def draw_sunken(window, player1_values, player2_values, Playerfleet, Computerfleet,number_of_sunk_ship_ai,number_of_sunk_ship_player):
        # Draw Player 1 sunken ships
        for ship in player1_values['player1_fleet'].keys():
            if player1_values['player1_fleet'][ship] == 0:
                for shipName in Playerfleet:
                    if shipName.name[0:2] == ship:
                        shipName.draw(window)
                        number_of_sunk_ship_player += 1

        # Draw Player 2 sunken ships
        for ship in player2_values['player2_fleet'].keys():
            if player2_values['player2_fleet'][ship] == 0:
                for shipName in Computerfleet:
                    if shipName.name[0:2] == ship:
                        shipName.draw(window)
                        number_of_sunk_ship_ai += 1
        # Display winner
        if number_of_sunk_ship_ai==7:
                font = pygame.font.SysFont("OCR-A Extended", 24)
                text = font.render("player won the game ", True, green)
                window.blit(text, (125,798))

        if number_of_sunk_ship_player==7:
            font = pygame.font.SysFont("OCR-A Extended", 24)
            text = font.render("AI won the game  ", True, red)
            window.blit(text, (125,798))

    # game utility functions
    def print_game_state() -> None:
        global copy_grids
        copy_grids = []

        # Function to print the current state of the game
        def create_grid_view(fleet, reference_grid):  # Create a grid view with ships placed on it

            # Initialize empty grid
            Vrows = rows
            Vcols = cols

            grid = [['..' for Cols in range(Vcols)] for rows in
                    range(Vrows)]  # Create an empty grid with dots representing empty cells in the grid (..)

            # Map ships to grid using grid coordinates
            for ship in fleet:

                # Calculate ship's starting grid position using the correct reference grid
                start_x = (ship.rect.x - reference_grid[0][0][0]) // CellSize
                start_y = (ship.rect.y - reference_grid[0][0][1]) // CellSize

                # Calculate ship length in cells
                if ship.rotation:  # Horizontal
                    length_x = ship.rect.width // CellSize  # Calculate the length of the ship in cells
                    length_y = 1  # Ship is horizontal, so length in y is 1
                else:  # Vertical
                    length_x = 1  # Ship is vertical, so length in x is 1
                    length_y = ship.rect.height // CellSize  # Calculate the length of the ship in cells

                # Fill all cells occupied by the ship

                for dx in range(length_x):  # Loop through the ship's length in x
                    for dy in range(length_y):  # Loop through the ship's length in y

                        x = start_x + dx  # Calculate the x coordinate of the cell
                        y = start_y + dy  # Calculate the y coordinate of the cell

                        # Check if the cell is within the grid boundaries
                        if 0 <= x < Vcols and 0 <= y < Vrows:  # Check if the cell is within the grid boundaries

                            grid[y][x] = f'{ship.name[:2]}'  # Fill the cell with the ship's name (first two characters)

            return grid

        def print_fleet_grid(fleet, reference_grid, title):
            global copy_grids
            print(f"\n=== {title} ===")

            # Print column headers
            print("   ", end="")
            for i in range(10):
                print(f"  {i} ", end="")
            print("\n")

            # Create and print grid with ships
            grid = create_grid_view(fleet, reference_grid)
            copy_grids.append(grid)
            for row_num, row in enumerate(grid):  # Loop through the grid rows

                print(f"{row_num:2d} ", end="")  # Print the row number with 2 digits (e.g., 01, 02, ..., 10)

                print("   ".join(row))  # Print the row with ships and empty cells (..)

            # Print ship coordinates and lengths
            print(f"\n{title} Ship Positions:")

            for ship in fleet:
                # Calculate ship's starting grid position using the correct reference grid
                start_x = (ship.rect.x - reference_grid[0][0][0]) // CellSize
                start_y = (ship.rect.y - reference_grid[0][0][1]) // CellSize

                # Calculate ship length in cells
                length = ship.rect.width // CellSize if ship.rotation else ship.rect.height // CellSize

                # Print ship name, starting position, orientation, and length
                orientation = "Horizontal" if ship.rotation else "Vertical"

                # Print ship name, starting position, orientation, and length
                print(f"{ship.name:12} at ({start_x}, {start_y}) - {orientation} - Length: {length}")

            print()

        # Print both player and computer grids using their respective reference grids
        print_fleet_grid(Playerfleet, pGameGrid, "Player Grid")
        print_fleet_grid(Computerfleet, cGameGrid, "Computer Grid")


    # show grid on screen function
    def ShowGridOnScreen(Window: pygame.surface, CellSize: int, PlayerGrid: list, ComputerGrid: list) -> None:
        # Draw the grid to the screen
        GameGrids = [PlayerGrid, ComputerGrid]

        for grid in GameGrids:
            if type(grid[0][0]) == tuple:
                # GameGrids = [PlayerGrid, ComputerGrid], grid = PlayerGrid or ComputerGrid
                for Row in grid:
                    # Row = [Col, Col, Col, Col, Col, Col, Col, Col, Col, Col]
                    for Col in Row:
                        # Col = [(y, x),(y, x),(y, x),(y, x),(y, x),(y, x),(y, x),(y, x),(y, x),(y, x)], Row = (y, x)

                        # (window, color, (y, x, width, height), thickness)
                        pygame.draw.rect(Window, white, (Col[0], Col[1], CellSize, CellSize), 1)


    def restart_game(): # Restart the game
        global game_started, game_over, resetGameGrid, player1_values, player2_values, Playerfleet,play_gameover_once, Computerfleet, scroll, game_paused, number_of_sunk_ship_ai, number_of_sunk_ship_player, copy_grids, ai_values, ai_turn

        # Reset game variables
        game_started = False
        game_over = False
        resetGameGrid = True
        game_paused = False
        play_gameover_once = True
        scroll = 0
        copy_grids = [[], []]

        # Reset player and computer grids
        set_grid_size(grid_size, grid_size)

        # Recreate player and computer fleets
        Playerfleet = createfleet()
        Computerfleet = createfleet()
        randomized_computer_ships(Computerfleet, cGameGrid)

        # Replay background theme
        pygame.mixer.music.play(-1)

        # Reset player values
        player1_values, player2_values, ai_turn = copyGrids()
        ai_values = {'shots_taken': [], 'unknown_cells': [], 'hit_cells': [], 'sunken_cells': [], 'last_hit': '',
                    'first_hit': False, 'tries': 0}
        number_of_sunk_ship_ai = 0
        number_of_sunk_ship_player = 0

    def restart_game_menu(): # Restart the game
        global game_started, game_over, resetGameGrid, player1_values, player2_values, Playerfleet,play_gameover_once, Computerfleet, scroll, game_paused, number_of_sunk_ship_ai, number_of_sunk_ship_player, copy_grids, ai_values, ai_turn

        # Reset game variables
        game_started = False
        game_over = False
        resetGameGrid = True
        game_paused = False
        play_gameover_once = True
        scroll = 0
        copy_grids = [[], []]

        # Reset player and computer grids
        set_grid_size(grid_size, grid_size)

        # Recreate player and computer fleets
        Playerfleet = createfleet()
        Computerfleet = createfleet()
        randomized_computer_ships(Computerfleet, cGameGrid)

        # Reset player values
        player1_values, player2_values, ai_turn = copyGrids()
        ai_values = {'shots_taken': [], 'unknown_cells': [], 'hit_cells': [], 'sunken_cells': [], 'last_hit': '',
                    'first_hit': False, 'tries': 0}
        number_of_sunk_ship_ai = 0
        number_of_sunk_ship_player = 0

    # setting button function
    def setting_button_function() -> bool:
        global game_paused, run_game

        game_paused = True  # Set the game to paused

        # button to resume the game and return to the game screen
        back_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Resume', 'Resume1.png')).convert_alpha()
        restart_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Restart', 'Restart1.png')).convert_alpha()
        fullscreen_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Fullscreen', 'Fullscreen1.png')).convert_alpha()
        quit_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Quit', 'Quit1.png')).convert_alpha()
        main_menu_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Main Menu', 'Main Menu1.png')).convert_alpha()
        volume_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Volume_button', 'Volume1.png')).convert_alpha()
        up_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Up', 'up_1.png')).convert_alpha()
        down_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Down', 'down_1.png')).convert_alpha()
        instructions_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Instructions', 'Instructions1.png')).convert_alpha()

        instructions_button = box_Button(settings_panel_rect.centerx - 150, settings_panel_rect.centery, instructions_img, settings_panel_rect.height, settings_panel_rect.width)
        main_menu_button = Button(settings_panel_rect.centerx, settings_panel_rect.bottom - 135, main_menu_img, settings_panel_rect.height, settings_panel_rect.width)
        quit_button = Button(settings_panel_rect.centerx, settings_panel_rect.bottom - 50, quit_img, settings_panel_rect.height, settings_panel_rect.width)
        restart_button = Button(settings_panel_rect.centerx, settings_panel_rect.bottom - 350, restart_img, settings_panel_rect.height, settings_panel_rect.width)
        back_button = Button(settings_panel_rect.centerx, settings_panel_rect.bottom - 450, back_img, settings_panel_rect.height, settings_panel_rect.width)
        fullscreen_button = Button(settings_panel_rect.centerx, settings_panel_rect.bottom - 250, fullscreen_img, settings_panel_rect.height, settings_panel_rect.width)
        volume_button = box_Button(settings_panel_rect.centerx + 150, settings_panel_rect.centery, volume_img, settings_panel_rect.height, settings_panel_rect.width)
        up_button = box_Button(settings_panel_rect.centerx + 150, settings_panel_rect.centery - 70, up_img, settings_panel_rect.height, settings_panel_rect.width)
        down_button = box_Button(settings_panel_rect.centerx + 150, settings_panel_rect.centery + 70, down_img, settings_panel_rect.height, settings_panel_rect.width)

        if down_button.rect.collidepoint(pygame.mouse.get_pos()):
            down_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Down', 'down_3.png')).convert_alpha()
            down_button = box_Button(settings_panel_rect.centerx + 150, settings_panel_rect.centery + 70, down_img, settings_panel_rect.height, settings_panel_rect.width)

        if up_button.rect.collidepoint(pygame.mouse.get_pos()):
            up_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Up', 'up_3.png')).convert_alpha()
            up_button = box_Button(settings_panel_rect.centerx + 150, settings_panel_rect.centery - 70, up_img, settings_panel_rect.height, settings_panel_rect.width)

        if volume_button.rect.collidepoint(pygame.mouse.get_pos()):
            volume_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Volume_button', 'Volume2.png')).convert_alpha()
            volume_button = box_Button(settings_panel_rect.centerx + 150, settings_panel_rect.centery, volume_img, settings_panel_rect.height, settings_panel_rect.width)
        
        if main_menu_button.rect.collidepoint(pygame.mouse.get_pos()):
            main_menu_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Main Menu', 'Main Menu3.png')).convert_alpha()
            main_menu_button = Button(settings_panel_rect.centerx, settings_panel_rect.bottom - 135, main_menu_img, settings_panel_rect.height, settings_panel_rect.width)

        if quit_button.rect.collidepoint(pygame.mouse.get_pos()):
            quit_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Quit', 'Quit3.png')).convert_alpha()
            quit_button = Button(settings_panel_rect.centerx, settings_panel_rect.bottom - 50, quit_img, settings_panel_rect.height, settings_panel_rect.width)

        if fullscreen_button.rect.collidepoint(pygame.mouse.get_pos()):
            fullscreen_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Fullscreen', 'Fullscreen3.png')).convert_alpha()
            fullscreen_button = Button(settings_panel_rect.centerx, settings_panel_rect.bottom - 250, fullscreen_img, settings_panel_rect.height, settings_panel_rect.width)

        if restart_button.rect.collidepoint(pygame.mouse.get_pos()):
            restart_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Restart', 'Restart3.png')).convert_alpha()
            restart_button = Button(settings_panel_rect.centerx, settings_panel_rect.bottom - 350, restart_img, settings_panel_rect.height, settings_panel_rect.width)

        if back_button.rect.collidepoint(pygame.mouse.get_pos()):
            back_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Resume', 'Resume3.png')).convert_alpha()
            back_button = Button(settings_panel_rect.centerx, settings_panel_rect.bottom - 450, back_img, settings_panel_rect.height, settings_panel_rect.width)

        if instructions_button.rect.collidepoint(pygame.mouse.get_pos()):
            instructions_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Instructions', 'Instructions3.png')).convert_alpha()
            instructions_button = box_Button(settings_panel_rect.centerx - 150, settings_panel_rect.centery, instructions_img, settings_panel_rect.height, settings_panel_rect.width)

        # Draw the settings panel on the screen
        overlay = pygame.Surface((ScreenWidth, ScreenHight))  # Create a transparent overlay
        overlay.fill((0, 0, 0))  # Fill the overlay with black color
        overlay.set_alpha(80)  # Set the transparency level
        GameScreen.blit(overlay, (0, 0))  # Draw the overlay on top of the screen
        GameScreen.blit(settings_panel, settings_panel_rect.topleft)
            
        # Draw buttons on settings panel
        if back_button.Draw(GameScreen):
            game_paused = False
        
        if restart_button.Draw(GameScreen):
            restart_game()

        if fullscreen_button.Draw(GameScreen):
            if pygame.display.get_surface().get_flags() & pygame.FULLSCREEN:
                pygame.display.set_mode((1260, 950))
            else:
                pygame.display.set_mode((1260, 950), pygame.FULLSCREEN)
        
        if quit_button.Draw(GameScreen):
            run_game = False
            sys.exit()

        if main_menu_button.Draw(GameScreen):
            run_game = False
            restart_game_menu()
            main_menu()
            

        if volume_button.Draw(GameScreen):
            pygame.mixer.music.pause() # Pause the background music


        if up_button.Draw(GameScreen):
            # Increase the volume by 0.01
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 1/100)
            pygame.mixer.music.unpause()

        if down_button.Draw(GameScreen):
            # Decrease the volume by 0.01
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 1/100)
            pygame.mixer.music.unpause()

        if instructions_button.Draw(GameScreen):
            instructions_Game()  # Will now return to settings panel after closing
            game_paused = True  # Keep the settings panel open
            
        pygame.display.update()  # Draw the settings panel on the screen

    # Update screen before and after placing ships
    def UpdateGameScreen(window: pygame.surface) -> None:
        global game_started, game_over, resetGameGrid, run_game, player1_values, player2_values, scroll, game_paused, play_gameover_once, start_button, setting_button, randomize_button, randomized, ai_values, ai_turn # Access the global game_started variable

        if game_paused:
            setting_button_function()
        
        if not game_paused:
            # Draw the scrolling background
            width = BG_img.get_width()
            for i in range(tiles):
                window.blit(BG_img, (i * width + scroll, 0))

            # Update the scroll position
            scroll -= 0.18

            # Reset scroll when it exceeds the width of one tile
            if abs(scroll) > width:
                scroll = 0

            # Fill window with black around the grids over the moving background
            window.fill(black,(0,0, pGameGrid[0][0][0],window.get_height()))
            window.fill(black, (0, 0,window.get_width() , pGameGrid[0][0][1]))
            window.fill(black, (0, (pGameGrid[len(pGameGrid)-1][len(pGameGrid)-1][0] + CellSize), window.get_width(), (pGameGrid[len(pGameGrid)-1][len(pGameGrid)-1][0] + CellSize)))
            window.fill(black, ((pGameGrid[len(pGameGrid)-1][len(pGameGrid)-1][1] + CellSize),0, ((cGameGrid[0][0][0]) - (pGameGrid[len(pGameGrid)-1][len(pGameGrid)-1][1] + CellSize)), window.get_height()))
            window.fill(black,((cGameGrid[len(cGameGrid)-1][len(cGameGrid)-1][0] + CellSize),0,window.get_width() ,window.get_height()))

            # Handle settings button hover
            if setting_button.rect.collidepoint(pygame.mouse.get_pos()):
                setting_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Settings', 'Settings3.png')).convert_alpha()
                setting_button = Button(ScreenXcenter, ScreenYcenter + ScreenHight // 15, setting_img, ScreenHight, ScreenWidth)
            else:
                setting_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Settings', 'Settings1.png')).convert_alpha()
                setting_button = Button(ScreenXcenter, ScreenYcenter + ScreenHight // 15, setting_img, ScreenHight, ScreenWidth)
            if setting_button.Draw(window):
                game_paused = True
            

            if not game_started:
                # Draw Grids to the screen
                ShowGridOnScreen(window, CellSize, pGameGrid, cGameGrid)
                
                # Draw Ships to the screen
                for ship in Playerfleet:
                    ship.draw(window)
                    ship.snap_to_grid(pGameGrid)

                # Draw Button to the screen
                if randomize_button.rect.collidepoint(pygame.mouse.get_pos()):
                    randomize_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Random', 'Random_3.png')).convert_alpha()
                    randomize_button = Button(ScreenXcenter, ScreenYcenter - 60, randomize_img, ScreenHight, ScreenWidth + 200)
                else:
                    randomize_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Random', 'Random_1.png')).convert_alpha()
                    randomize_button = Button(ScreenXcenter, ScreenYcenter - 60, randomize_img, ScreenHight, ScreenWidth + 200)
                
                randomize_button.Draw(window)
                clicked = pygame.mouse.get_pressed()
                if clicked[0]:
                    if randomize_button.rect.collidepoint(pygame.mouse.get_pos()):
                        if randomized:
                            randomized_computer_ships(Playerfleet, pGameGrid)
                            randomized = False
                else:
                    randomized = True

                if all_ships_placed() and not game_started:
                    if start_button.rect.collidepoint(pygame.mouse.get_pos()):
                        start_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Start', 'Start3.png')).convert_alpha()
                        start_button = Button(ScreenXcenter, ScreenYcenter, start_img, ScreenHight, ScreenWidth + 200)
                    else:
                        start_img = pygame.image.load(os.path.join(DIRS['buttons'], 'Start', 'Start1.png')).convert_alpha()
                        start_button = Button(ScreenXcenter, ScreenYcenter, start_img, ScreenHight, ScreenWidth + 200)

                    if start_button.Draw(window):
                        game_started = True
                        print_game_state()
                        player1_values, player2_values, ai_turn = copyGrids()


            else:  # the game started
                if not game_over:
                    # Draw Grids to the screen
                    ShowGridOnScreen(window, CellSize, pGameGrid, cGameGrid)

                    # Draw Ships to the screen
                    for ship in Playerfleet:
                        ship.draw(window)
                        ship.snap_to_grid(pGameGrid)

                    draw_sunken(window, player1_values, player2_values, Playerfleet, Computerfleet,number_of_sunk_ship_ai,number_of_sunk_ship_player)
                    draw_shots(window, player1_values, player2_values)
                    display_turn(GameScreen, player2_values['player2Turn'], player2_values['player2Turn'],ai_img,player_img)

                    # let Ai take shot
                    if ai_vs_player:
                        if player2_values['player2Turn'] or not player1_values['player1Turn']:
                            try:
                                xCooForShots, yCooForShots, ai_turn.ai_values = ai_turn.fire()
                                shot = search_hit(yCooForShots, xCooForShots, player1_values, player2_values, game_over)
                                player1_values, player2_values, game_over = shot[1], shot[2], shot[3]
                                if player1_values['player1Grid'][yCooForShots][xCooForShots] == 'H':
                                    hit_sound.play()
                                if player1_values['player1Grid'][yCooForShots][xCooForShots] == 'S':
                                    sunk_sound.play()
                                if player1_values['player1Grid'][yCooForShots][xCooForShots] == 'M':
                                    miss_sound.play()
                            except:
                                pass

                else:
                    # Play game over sound once
                    if play_gameover_once:
                        hit_sound.stop()
                        miss_sound.stop()
                        sunk_sound.stop()
                        pygame.mixer.music.stop()
                        gameover_sound.play()
                        if player1_values['player1Turn']:
                            player_lose_sound.play()
                        else:
                            player_win_sound.play()

                        play_gameover_once = False


                    # Draw Grids to the screen
                    ShowGridOnScreen(window, CellSize, pGameGrid, cGameGrid)

                    # Draw Ships to the screen
                    for ship in Playerfleet:
                        ship.draw(window)
                        ship.snap_to_grid(pGameGrid)

                    draw_sunken(window, player1_values, player2_values, Playerfleet, Computerfleet, number_of_sunk_ship_ai, number_of_sunk_ship_player)
                    draw_shots(window, player1_values, player2_values)

                    font = pygame.font.SysFont("OCR-A Extended", 100)
                    text = font.render("GAME OVER", True, green)
                    text_pos = (350, 600)
                    window.blit(text, text_pos)
                    
            window.blit(BG_border, (0, 0))
            # Update the display
        pygame.display.flip()

    # - - - - - - - - Initialise players - - - - - - - - -
    # create player fleet
    Playerfleet = createfleet()

    # create computer fleet
    Computerfleet = createfleet()
    randomized_computer_ships(Computerfleet, cGameGrid)

    # - - - - - - - - - - - - Main Game Loop - - - - - - - - - - - - -
    # Initialize running game
    run_game = True


    # Events handler
    def handle_events() -> None:
        global run_game, yCooForShots, xCooForShots, game_over, player1_values, player2_values, game_paused
        
        
        # for loop to handle events in the game
        for event in pygame.event.get():

            # check if the event is a quit event
            if event.type == pygame.QUIT:
                # set run_game to False for exiting the game loop
                run_game = False
                sys.exit()

            elif event.type == pygame.KEYDOWN:  # Check if a key is pressed
                if event.key == pygame.K_r and not game_started:  # Check if the key pressed is the 'R' key
                    randomized_computer_ships(Playerfleet, pGameGrid)  # Randomize player's ships



            # check if the event is a mouse button down event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started:
                    if event.button == 1:  # check if the mouse button pressed was the left mouse button
                        # call the handle_ship_selection function to handle ship selection
                        handle_ship_selection()
                        UpdateGameScreen(GameScreen)


                else:  # if the game started
                    if event.button == 1:  # check if the mouse button pressed was the left mouse button
                        if not game_over and not game_paused:
                            xCooForShots, yCooForShots = pygame.mouse.get_pos()  # Get mouse's position
                            
                            # Player 1's turn
                            if player1_values['player1Turn'] and cGameGrid[0][0][0] <= xCooForShots <= \
                                    cGameGrid[grid_size - 1][grid_size - 1][0] + CellSize and cGameGrid[0][0][
                                1] <= yCooForShots <= cGameGrid[grid_size - 1][grid_size - 1][1] + CellSize:
                                
                                # Calculate grid coordinates relative to grid origin
                                xCooForShots = (xCooForShots - cGameGrid[0][0][0]) // CellSize
                                yCooForShots = (yCooForShots - cGameGrid[0][0][1]) // CellSize
                                
                                # Validate coordinates are within grid bounds
                                if 0 <= xCooForShots < grid_size and 0 <= yCooForShots < grid_size:
                                    try:
                                        shot = search_hit(yCooForShots, xCooForShots, player1_values, player2_values, game_over)
                                        player1_values, player2_values, game_over = shot[1], shot[2], shot[3]
                                        
                                        # Play appropriate sound effect
                                        if player2_values['player2Grid'][yCooForShots][xCooForShots] == 'H':
                                            hit_sound.play()
                                        elif player2_values['player2Grid'][yCooForShots][xCooForShots] == 'S':
                                            sunk_sound.play()
                                        elif player2_values['player2Grid'][yCooForShots][xCooForShots] == 'M':
                                            miss_sound.play()
                                            
                                        now = pygame.time.get_ticks()
                                        ai_turn.last = now
                                    except:
                                        pass

                            # Player 2's turn (if not AI vs player)
                            if not ai_vs_player:
                                if player2_values['player2Turn'] and pGameGrid[0][0][0] <= xCooForShots <= \
                                        pGameGrid[grid_size - 1][grid_size - 1][0] + CellSize and pGameGrid[0][0][
                                    1] <= yCooForShots <= pGameGrid[grid_size - 1][grid_size - 1][1] + CellSize:
                                    
                                    # Use same calculation method as player 1
                                    xCooForShots = (xCooForShots - pGameGrid[0][0][0]) // CellSize
                                    yCooForShots = (yCooForShots - pGameGrid[0][0][1]) // CellSize
                                    
                                    # Validate coordinates are within grid bounds
                                    if 0 <= xCooForShots < grid_size and 0 <= yCooForShots < grid_size:
                                        try:
                                            shot = search_hit(yCooForShots, xCooForShots, player1_values, player2_values, game_over)
                                            player1_values, player2_values, game_over = shot[1], shot[2], shot[3]
                                        except:
                                            pass
    while run_game:
        clock.tick(60)
        handle_events()
        UpdateGameScreen(GameScreen)

    pygame.quit()
main_menu()