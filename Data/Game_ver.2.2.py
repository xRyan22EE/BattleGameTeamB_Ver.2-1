#  - - - - - - - - - - - - - - - - - - Modules Import - - - - - - - - - - - - - - - - - -
# Import functions from game's files
from grid import CreateGameGrid
from game_utils import LoadImage
from Buttons import Button
from Display_Turns import display_turn
from search_system import search_hit
from BG import moving_background, draw_scrolling_background

# Import modules
import pygame
import random
import copy
import math
import os
import time
# - - - - - - - - - - - - - - - - - - Initialization - - - - - - - - - - - - - - - - - -

# set main directory to the whole project's file
assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(assets_dir)

# module Initialization
pygame.init()

# game variables
clock = pygame.time.Clock()
game_started = False # variable to check if the game has started
game_paused = False # variable to check if the game is paused

# Game Settings and Variables
ScreenWidth = 1920
ScreenHight = 1080
# 1260
# 960
#1920
#1080

grid_size = 15
resetGameGrid = True
game_over = False
 
# Set first shot out of boundaries till the user input
yCooForShots = grid_size +1
xCooForShots = grid_size +1

# Set the first turn


# Set colors (R,G,B)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
orange = (245, 145, 30)

# Colors of shots taken
colors = {
    '..': black,
    'S': red,
    'H': orange,
    'M': blue}

# pygame display Initialization

GameScreen = pygame.display.set_mode((ScreenWidth, ScreenHight-10),pygame.FULLSCREEN)

# disply variable for the game screen
ScreenXcenter = GameScreen.get_rect().centerx # get the center of the screen width
ScreenYcenter = GameScreen.get_rect().centery # get the center of the screen hight

# background image path and variables
image_path = 'images/BG/download.png'
BG_width, BG_tiles, BG_img = moving_background(image_path, ScreenWidth)



# set the title of the window
pygame.display.set_caption("Battle Ship Demo")

# Game Lists/Dictionaries

# Initialize copy of players grids, where copy_grids[0] is a list for player 1, and copy_grids[1] is a list for player 2
copy_grids = [[],[]]

# Players_fleet  = Player Fleet Dictionary     key: [name, image path, position, size, health]
Players_fleet = {
    "carrier": ["carrier", "images/ships/carrier/carrier.png", (50, 600), 5],
    "battleship": ["battleship", "images/ships/battleship/battleship.png", (125, 600), 4],
    "cruiser": ["cruiser", "images/ships/cruiser/cruiser.png", (200, 600), 4],
    "destroyer": ["destroyer", "images/ships/destroyer/destroyer.png", (275, 600), 3],
    "submarine": ["submarine", "images/ships/submarine/submarine.png", (350, 600), 3],
    "patrol boat": ["patrol boat", "images/ships/patrol boat/patrol boat.png", (425, 600), 2],
    "rescue ship": ["rescue ship", "images/ships/rescue ship/rescue ship.png", (500, 600), 2]
}

# Set Players Ship's Health, where each key represents the firs two letters of the ship's name
Player1Health = {
    "ca": 5, "ba": 4, "cr": 4, "de": 3, "su": 3, "pa": 2, "re": 2}

Player2Health = {
    "ca": 5, "ba": 4, "cr": 4, "de": 3, "su": 3, "pa": 2, "re": 2}

# loading game variables

# loading game sound and Image
start_img = pygame.image.load("images/Button/start_btn.png").convert_alpha()
exit_img = pygame.image.load("images/Button/exit_btn.png").convert_alpha()
setting_img = pygame.image.load("images/Button/settings_icon.png").convert_alpha()


# - - - - - - - - - - - - - - Buttons - - - - - - - - - - - - - -

# Button instance for start and exit button
start_button = Button(ScreenXcenter, ScreenYcenter, start_img, ScreenHight, ScreenWidth)
# exit_button = Button(ScreenWidth // 2, (ScreenHight // 2) + ScreenWidth // 25, exit_img, ScreenHight, ScreenWidth)
setting_button = Button(ScreenXcenter, ScreenYcenter + ScreenHight // 15, setting_img, ScreenHight, ScreenWidth)
settings_panel = pygame.Surface((600, 500))
settings_panel.fill((50, 50, 50))  # Dark gray background
settings_panel_rect = settings_panel.get_rect(center=(ScreenXcenter, ScreenYcenter)) # Center the panel on the screen

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
        global raws, cols, CellSize, pGameGrid, pGameLogic, cGameGrid, cGameLogic
        raws = new_rows
        cols = new_cols

        # Calculate CellSize based on grid dimensions
        CellSize = min(ScreenWidth // cols, ScreenHight // (2 * raws))
        # Re-create the player and computer grids
        pGameGrid = CreateGameGrid(raws, cols, CellSize, (50, 50))
        cGameGrid = CreateGameGrid(raws, cols, CellSize, (((ScreenWidth - 50) - (cols * CellSize)), 50))

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
        grid_start_x = grid[0][0][0]  # Grid's left boundary
        grid_end_x = grid[0][-1][0]   # Grid's right boundary
        grid_start_y = grid[0][0][1]  # Grid's top boundary
        grid_end_y = grid[-1][0][1]   # Grid's bottom boundary

        if self.CheckinGrid(pGameGrid):
            for row in grid:
                for col in row:
                    cell_top_left_x = col[0]
                    cell_top_left_y = col[1]
                    # Skip cells that would cause ship to go out of bounds
                    if self.rotation:
                        if cell_top_left_x + cells_required_x * CellSize > grid_end_x + CellSize:
                            continue
                    else:
                        if cell_top_left_y + cells_required_y * CellSize > grid_end_y + CellSize:
                            continue

                    distance = ((current_top_left[0] - cell_top_left_x) ** 2 + 
                              (current_top_left[1] - cell_top_left_y) ** 2) ** 0.5

                    if distance < min_distance:
                        min_distance = distance
                        closest_cell_top_left = (cell_top_left_x, cell_top_left_y)

            if closest_cell_top_left:
                # Verify the ship will fit within grid boundaries
                if self.rotation:
                    if (closest_cell_top_left[0] >= grid_start_x and 
                        closest_cell_top_left[0] + cells_required_x * CellSize <= grid_end_x + CellSize):
                        self.rect.topleft = closest_cell_top_left
                        self.rect.centerx = closest_cell_top_left[0] + (cells_required_x * CellSize) // 2
                        self.rect.centery = closest_cell_top_left[1] + CellSize // 2
                    else:
                        self.return_to_start()
                else:
                    if (closest_cell_top_left[1] >= grid_start_y and 
                        closest_cell_top_left[1] + cells_required_y * CellSize <= grid_end_y + CellSize):
                        self.rect.topleft = closest_cell_top_left
                        self.rect.centerx = closest_cell_top_left[0] + CellSize // 2
                        self.rect.centery = closest_cell_top_left[1] + (cells_required_y * CellSize) // 2
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
                distance = ((current_top_left[0] - cell_top_left_x) ** 2 + (current_top_left[1] - cell_top_left_y) ** 2) ** 0.5

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
def createfleet() -> list:
    fleet = []
    for name, (img_name, img_path, pos, cell_count) in Players_fleet.items():
        # Calculate the ship size in pixels based on CellSize and cell count
        if name != "patrol boat" and name != "rescue ship":
            adjusted_size = (CellSize, cell_count * CellSize)
        else:
            adjusted_size = (CellSize*0.65, CellSize * cell_count)
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

def all_ships_placed() -> bool:
    # Check if all ships are placed in the grid

    # Return True if all ships are placed in the grid, otherwise return False
    return all(ship.is_placed_in_grid() for ship in Playerfleet)

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

# - - - - - - - - - - Turns based System - - - - - - - - - - -

# - - - - - - - - Search for Hits System - - - - - - - - -

# - - - - - - - - Game Utility Functions - - - - - - - - -

# setting button function
def setting_button_function() -> bool:
    game_paused = True # Set the game to paused
    overlay = pygame.Surface((ScreenWidth, ScreenHight)) # Create a transparent overlay 
    overlay.fill((0, 0, 0)) # Fill the overlay with black color
    overlay.set_alpha(80)  # Set the transparency level
    GameScreen.blit(overlay, (0, 0))  # Draw the overlay on top of the screen

    GameScreen.blit(settings_panel, settings_panel_rect.topleft)  # Draw the settings panel on the screen
    return game_paused

# Set grid size based on user input
def set_grid_size(new_rows: int, new_cols: int) -> None:
    # function to set grid size and dynamically adjust cell size
    global raws, cols, CellSize, pGameGrid, pGameLogic, cGameGrid, cGameLogic
    raws = new_rows
    cols = new_cols

    # divide ScreenHight by 2 to leave space for both grids and divide by raws to get the cell size for the grid
    CellSize = min(ScreenWidth // cols, ScreenHight // (2 * raws))
    # create game grid for player and computer grid with the new raws, cols and cell size
    pGameGrid = CreateGameGrid(raws, cols, CellSize, (50, 50))
    cGameGrid = CreateGameGrid(raws, cols, CellSize, (((ScreenWidth - 50) - (cols * CellSize)), 50))

# Make a copy of players grids to calculate hits
def copyGrids():
    # Set start of game values

    # Player 1 values
    player1Grid = copy.deepcopy(copy_grids[0])
    player1_reference = copy.deepcopy(copy_grids[0])
    player1_fleet = Player1Health
    # Randomise players turns
    player1Turn = True

    # Player 2 values
    player2Grid = copy.deepcopy(copy_grids[1])
    player2_reference = copy.deepcopy(copy_grids[1])
    player2_fleet = Player2Health
    # Set player 2 turn as the opposite of player 1
    player2Turn = not player1Turn

    # Set lists for each player
    player1_values = {'player1Grid': player1Grid, 'player1_reference': player1_reference, 'player1_fleet': player1_fleet, 'player1Turn': player1Turn}
    player2_values = {'player2Grid': player2Grid, 'player2_reference': player2_reference, 'player2_fleet': player2_fleet, 'player2Turn': player2Turn}
    return player1_values,player2_values

# Draw shots indicators
def draw_shots(player1_values, player2_values):
    # Draw all grid with shots or without
    # Used try & except to not draw on ships
    for row in range(len(player2_values['player2Grid'])):
        for col in range(len(player2_values['player2Grid'][row])):
            xCooForShots = col
            yCooForShots = row
            try:
                pygame.draw.circle(GameScreen, colors[player2_values['player2Grid'][row][col]], (cGameGrid[yCooForShots][xCooForShots][0] + CellSize // 2,cGameGrid[yCooForShots][xCooForShots][1] + CellSize // 2),CellSize // 4)
            except:
                pass
    for row in range(len(player1_values['player1Grid'])):
        for col in range(len(player1_values['player1Grid'][row])):
            xCooForShots = col
            yCooForShots = row
            try:
                pygame.draw.circle(GameScreen, colors[player1_values['player1Grid'][row][col]], (pGameGrid[yCooForShots][xCooForShots][0] + CellSize // 2,pGameGrid[yCooForShots][xCooForShots][1] + CellSize // 2),CellSize // 4)
            except:
                pass

# game utility functions
def print_game_state() -> None:
    global copy_grids
    copy_grids = []

    # Function to print the current state of the game
    def create_grid_view(fleet, reference_grid):  # Create a grid view with ships placed on it

        # Initialize empty grid
        Vrows = raws
        Vcols = cols

        grid = [['..' for Cols in range(Vcols)] for Raws in
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
                    # Col = [(yCooForShots, xCooForShots),(yCooForShots, xCooForShots),(yCooForShots, xCooForShots),(yCooForShots, xCooForShots),(yCooForShots, xCooForShots),(yCooForShots, xCooForShots),(yCooForShots, xCooForShots),(yCooForShots, xCooForShots),(yCooForShots, xCooForShots),(yCooForShots, xCooForShots)], Row = (yCooForShots, xCooForShots)

                    # (window, color, (yCooForShots, xCooForShots, width, height), thickness)
                    pygame.draw.rect(Window, white, (Col[0], Col[1], CellSize, CellSize), 1)
        # else: # Draw shots grid
        #     for i, row in enumerate(grid):
        #         for j, cell in enumerate(row):
        #             pygame.draw.rect(Window, white, (i, j, CellSize, CellSize), 1)

# Define scrolling background variables
scroll = 0
tiles = 2  # Number of tiles to cover the screen width

# Load the background image
bg_img = pygame.image.load("images/BG/download.png").convert()

# Update screen before and after placing ships
def UpdateGameScreen(window: pygame.surface) -> None:
    global game_started, game_over, resetGameGrid, run_game, player1_values, player2_values, scroll, game_paused # Access the global game_started variable

    # Draw the scrolling background
    width = bg_img.get_width()
    for i in range(tiles):
        window.blit(bg_img, (i * width + scroll, 0))
    
    # Update the scroll position
    scroll -= 5

    # Reset scroll when it exceeds the width of one tile
    if abs(scroll) > width:
        scroll = 0

    if not game_started:
        # Draw Grids to the screen
        ShowGridOnScreen(window, CellSize, pGameGrid, cGameGrid)

        # Draw Ships to the screen
        for ship in Playerfleet:
            ship.draw(window)
            ship.snap_to_grid(pGameGrid)

        for ship in Computerfleet:
            ship.draw(window)

        # Draw Button to the screen
        if all_ships_placed() and not game_started:
            if start_button.Draw(window):
                game_started = True
                print_game_state()
                player1_values, player2_values = copyGrids()

        random_font = pygame.font.SysFont("OCR-A Extended", 27) # Set the font style and size
        text = random_font.render("Press R for rnadom", True, red) # Render the text to the screen
        text_pos = (50, 20) # Set the position of the text 
        window.blit(text, text_pos) 

        if setting_button.Draw(window) or game_paused: # Check if the setting button is clicked or the game is paused
            game_paused = setting_button_function()


    else:  # the game started

        if not game_over:
            # Draw Grids to the screen
            ShowGridOnScreen(window, CellSize, pGameGrid, cGameGrid)

            # Draw Ships to the screen
            for ship in Playerfleet:
                ship.draw(window)
                ship.snap_to_grid(pGameGrid)
            
            if setting_button.Draw(window) or game_paused:
                game_paused = True
                setting_button_function()          
            
            if not game_paused:
                draw_shots(player1_values, player2_values)
                display_turn(GameScreen, player2_values['player2Turn'], player2_values['player2Turn'])
        
        elif game_over:
            draw_shots(player1_values, player2_values)
            font = pygame.font.SysFont("OCR-A Extended", 100)
            text = font.render("GAME OVER", True, green)
            text_pos = (350, 600)
            window.blit(text, text_pos)

    # Update the display
    pygame.display.flip()
# - - - - - - - - Initialize Game's Grids - - - - - - - -

# set the grid size for the game (rows, cols)
set_grid_size(grid_size, grid_size)

# Initialise players

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
        
        elif event.type == pygame.KEYDOWN: # Check if a key is pressed 
            if event.key == pygame.K_r and not game_started:# Check if the key pressed is the 'R' key
                randomized_computer_ships(Playerfleet, pGameGrid) # Randomize player's ships
            elif event.key == pygame.K_ESCAPE:
                game_paused = not game_paused

        # check if the event is a mouse button down event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started:
                if event.button == 1: # check if the mouse button pressed was the left mouse button
                    # call the handle_ship_selection function to handle ship selection
                    handle_ship_selection()
                    UpdateGameScreen(GameScreen)

            else: # if the game started
                if event.button == 1: # check if the mouse button pressed was the left mouse button
                        if not game_over and not game_paused:
                            xCooForShots , yCooForShots = pygame.mouse.get_pos() # Get mouse's position
                            # Based on turns, make borders around the appropriate grid, calculate which cell the mouse clicked
                            if player1_values['player1Turn'] and cGameGrid[0][0][0] <= xCooForShots <= cGameGrid[grid_size-1][grid_size-1][0] + CellSize and cGameGrid[0][0][1] <= yCooForShots <= cGameGrid[grid_size-1][grid_size-1][1] + CellSize:
                                xCooForShots = math.floor((xCooForShots // CellSize) - (grid_size*1.5))
                                yCooForShots = math.ceil((yCooForShots // CellSize) - (grid_size*0.1))
                                shot = search_hit(yCooForShots, xCooForShots, player1_values, player2_values, game_over)
                                player1_values, player2_values, game_over = shot[1], shot[2], shot[3]

                            # We can implement random Ai down here or any where else
                            elif player2_values['player2Turn'] and pGameGrid[0][0][0] <= xCooForShots <= pGameGrid[grid_size-1][grid_size-1][0] + CellSize and pGameGrid[0][0][1] <= yCooForShots <= pGameGrid[grid_size-1][grid_size-1][1] + CellSize:
                                xCooForShots = math.floor((xCooForShots // CellSize) - 1 )
                                yCooForShots = math.ceil((yCooForShots // CellSize) - 1)
                                shot = search_hit(yCooForShots, xCooForShots, player1_values, player2_values, game_over)
                                player1_values, player2_values, game_over = shot[1], shot[2], shot[3]


# Main game loop

while run_game:
    clock.tick(60)
    handle_events()
    UpdateGameScreen(GameScreen)


pygame.quit()