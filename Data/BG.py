import pygame
import math
pygame.init()

# Global variables
ScreenWidth = 1260
ScreenHight = 960
scroll = 0
clock = pygame.time.Clock()
# run = True
image_path = 'images/BG/download.png'

# # Initialize screen
# screen = pygame.display.set_mode((ScreenWidth, ScreenHight))
# pygame.display.set_caption("Background Test")


def moving_background(image_path, ScreenWidth):
  
    #Loads the background image and calculates width and tiles needed.
   
    img = pygame.image.load(image_path).convert()
    width = img.get_width()
    tiles = math.ceil(ScreenWidth / width) + 1  # Number of tiles to cover the screen
    return width, tiles, img


def draw_scrolling_background(screen, img, scroll, tiles, width):

    #Draws the scrolling background on the screen and updates the scroll position.
 
    for i in range(tiles):
        screen.blit(img, (i * width + scroll, 0))
    
    # Update the scroll position
    scroll -= 5

    # Reset scroll when it exceeds the width of one tile
    if abs(scroll) > width:
        scroll = 0

    return scroll


# # Initialize background variables
# width, tiles, img = moving_background(image_path, ScreenWidth)

# # Game loop
# while True:
#     clock.tick(60)
    
#     # Draw the scrolling background and update the scroll position
#     scroll = draw_scrolling_background(screen, img, scroll, tiles, width)

#     # Event handling
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
    
#     pygame.display.update()

# pygame.quit()
