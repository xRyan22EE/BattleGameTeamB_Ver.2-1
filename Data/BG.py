import pygame
import math

from pygame.transform import rotate

pygame.init()

# Global variables
clock = pygame.time.Clock()

def moving_background(image_path, ScreenWidth, ScreenHight):
  
    #Loads the background image and calculates width and tiles needed.
    img = pygame.image.load(image_path).convert()
    adjusted_img = pygame.transform.scale(img, (img.get_width(), ScreenHight))
    width = adjusted_img.get_width()
    tiles = math.ceil(ScreenWidth / width) + 1  # Number of tiles to cover the screen
    return width, tiles, adjusted_img

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
