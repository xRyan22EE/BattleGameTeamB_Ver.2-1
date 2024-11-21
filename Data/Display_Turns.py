import pygame

def display_turn(screen, player1Turn, player2Turn, player_img, ai_img):

    if not player1Turn:
        screen.blit(ai_img, ai_img.get_rect(center=(screen.get_width()//2, 60)))
    else:
        screen.blit(player_img, player_img.get_rect(center=(screen.get_width()//2, 60)))




