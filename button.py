import pygame
import os
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

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

BUTTONSTATES = {True: "black", False: "White"}

class Slider():
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int) -> None:
        self.pos = pos
        self.size = size
        self.hovered = False
        self.grabbed = False

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max
        self.button_width = 20  # Set the button width here
        self.initial_val = (self.slider_right_pos - self.slider_left_pos - self.button_width) * initial_val  # Adjust for button width

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val, self.slider_top_pos, self.button_width, self.size[1])

        # label
        self.text = pygame.font.Font(os.path.join(DIRS["assets"],"font.ttf"), 25).render(str(int(self.get_value())), True, "white", None)
        self.label_rect = self.text.get_rect(center=(self.pos[0], self.slider_top_pos - 15))

    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos + self.button_width // 2:
            pos = self.slider_left_pos + self.button_width // 2
        if pos > self.slider_right_pos - self.button_width // 2:
            pos = self.slider_right_pos - self.button_width // 2
        self.button_rect.centerx = pos  # Adjust the centerx position directly

    def hover(self):
        self.hovered = True

    def render(self, app):
        pygame.draw.rect(app, "Green", self.container_rect)
        pygame.draw.rect(app, BUTTONSTATES[self.hovered], self.button_rect)

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - self.button_width  # Adjust for button width
        button_val = self.button_rect.centerx - self.slider_left_pos - self.button_width // 2

        return (button_val / val_range) * (self.max - self.min) + self.min

    def display_value(self, app):
        self.text = pygame.font.Font(os.path.join(DIRS["assets"],"font.ttf"), 25).render(str(int(self.get_value())), True, "white", None)
        app.blit(self.text, self.label_rect)
