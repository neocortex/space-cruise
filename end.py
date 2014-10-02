import pygame
import random


def draw_end(screen, background, stars):
    """ Draw the game over screen. """
    background.fill((0, 0, 0))
    pos = [(0, 0), (-1, 0), (0, -1), (1, 0), (0, 1)]
    for x, y in stars:
        for i, j in pos:
            background.set_at(
                (x+i, y+j), (random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255)))
    # Draw enter message
    title_font = pygame.font.SysFont(u'tlwgtypewriter', 50)
    start_str = title_font.render("GAME OVER", True, (255, 255, 255))
    background.blit(start_str, (
        background.get_rect().centerx - start_str.get_width() / 2,
        background.get_rect().centery - 50))
    screen.blit(background, (0, 0))
    pygame.display.flip()
