import pygame
import random


def draw_title(screen, background, stars, draw_msg=True):
    """ Draw the screen title. Includes the title pixel image, the background
        stars, and the enter message.

    """
    background.fill((0, 0, 0))
    # Draw stars
    pos = [(0, 0), (-1, 0), (0, -1), (1, 0), (0, 1)]
    for x, y in stars:
        for i, j in pos:
            background.set_at(
                (x+i, y+j), (random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255)))
    # Blit title image
    title_im = pygame.image.load('images/cruiser.png')
    background.blit(title_im, (
        (background.get_rect().centerx - title_im.get_width() / 2),
        background.get_rect().centery - title_im.get_height() / 2))
    # Draw enter message
    title_font = pygame.font.SysFont(u'tlwgtypewriter', 20)
    start_str = title_font.render("PRESS  ENTER", True, (255, 255, 255))
    if draw_msg:
        background.blit(start_str, (
            background.get_rect().centerx - start_str.get_width() / 2,
            background.get_rect().bottom - 80))
    screen.blit(background, (0, 0))
    pygame.display.flip()


def title_stars(background, n=500):
    """ Return random positions for stars on title screen. """
    xpos = [random.randint(2, background.get_width() - 2) for _ in xrange(n)]
    ypos = [random.randint(2, background.get_height() - 2) for _ in xrange(n)]
    return zip(xpos, ypos)
