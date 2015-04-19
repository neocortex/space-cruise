import pygame
import random


def draw_end(screen, background, stars, display_txt):
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
    over_str = title_font.render("GAME OVER", True, (255, 255, 255))
    background.blit(over_str, (
        background.get_rect().centerx - over_str.get_width() / 2,
        background.get_rect().centery - 100))
    # Draw result text
    display_txt.set_pos(
        (background.get_rect().centerx - display_txt.text_rect.width / 2,
         background.get_rect().centery))
    display_txt.draw()
    screen.blit(background, (0, 0))
    pygame.display.flip()
