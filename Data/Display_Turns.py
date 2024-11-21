import pygame

def display_turn(screen, player1Turn, player2Turn,):
    font = pygame.font.SysFont("Arial", 24)
    turn_text = ''
    color = (0, 0, 0)
    # Determine Turn Text
    if not player1Turn:
        turn_text = "Player 1's Turn"
        color = (0, 255, 0)  # Green
    else:
        turn_text = "Player 2's Turn"
        color = (255, 0, 0)  # Red

    # Render Text
    turn_surface = font.render(turn_text, True, color)
    turn_surface_rect = turn_surface.get_rect(center = (1260//2, 960//2))

    # Blit Text to Screen
    screen.blit(turn_surface, turn_surface_rect)

print(1160/ 2 - 15)



