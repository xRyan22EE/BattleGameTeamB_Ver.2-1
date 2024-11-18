import pygame
import time 
# A class to create buttons
class Button:

    def __init__(self, x: int, y: int, content, screen_height=None, screen_width=None) -> None:
        # Initialize font
        self.font = pygame.font.SysFont('Arial', 30)
        
        # Handle both image and text buttons
        if isinstance(content, str):
            # Create text surface
            self.image = self.font.render(content, True, (255, 255, 255))
            self.button_width = self.image.get_width() + 20  # Add padding
            self.button_height = self.image.get_height() + 10
        else:
            # Handle image button
            self.image = content
            if screen_width and screen_height:
                self.button_width = screen_width // 10
                self.button_height = screen_height // 15
                self.image = pygame.transform.scale(self.image, (self.button_width, self.button_height))

        # Create button rectangle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Button state
        self.clicked = False

    def Draw(self, surface: pygame.Surface) -> bool:
        action = False
        
        # Get mouse position
        pos = pygame.mouse.get_pos()
        
        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        # Draw button
        surface.blit(self.image, self.rect)
        
        return action