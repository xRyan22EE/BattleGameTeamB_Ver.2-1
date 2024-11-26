import pygame, os

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

DIRS = setup_directories()

def get_font(size):  # Returns Press-Start-2P in the desired size
    font_path = os.path.join(DIRS['assets'], 'font.ttf')
    try:
        return pygame.font.Font(font_path, size)
    except OSError:
        print(f"Warning: Could not load font at {font_path}")
        return pygame.font.SysFont("Arial", size)