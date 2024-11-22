import pygame

def LoadImage(path, size, rotate=False):
    # A function to import Images Into memory
    img = pygame.image.load(path).convert_alpha()

    # Scale the image
    img = pygame.transform.scale(img, size)

    # Rotate the image
    if rotate:
        img = pygame.transform.rotate(img, -90)
    return img

