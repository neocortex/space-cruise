import pygame
import random


class EndScreen(object):

    def __init__(self, screen, background, clock, display_txt):
        self.screen = screen
        self.background = background
        self.clock = clock
        self.display_txt = display_txt
        self.stars = self.make_stars()
        self.end_font = pygame.font.SysFont(u'tlwgtypewriter', 50)
        self.over_str = self.end_font.render(
            "GAME OVER", True, (255, 255, 255))

    def draw_end(self):
        """ Draw the game over screen. """
        self.background.fill((0, 0, 0))
        pos = [(0, 0), (-1, 0), (0, -1), (1, 0), (0, 1)]
        for x, y in self.stars:
            for i, j in pos:
                self.background.set_at(
                    (x+i, y+j), (random.randint(0, 255),
                                 random.randint(0, 255),
                                 random.randint(0, 255)))
        self.background.blit(self.over_str, (
            self.background.get_rect().centerx - self.over_str.get_width() / 2,
            self.background.get_rect().centery - 100))
        # Draw result text
        self.display_txt.set_pos(
            (self.background.get_rect().centerx - self.display_txt.text_rect.width / 2,
            self.background.get_rect().centery))
        self.display_txt.draw()
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def end_loop(self):
        """ The game over loop. """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        running = False
                        return 'restart'
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        return 'quit'
            self.clock.tick(100)
            self.draw_end()

    def make_stars(self, n=500):
        """ Return random positions for stars on title screen. """
        xpos = [random.randint(
            2, self.background.get_width() - 2) for _ in xrange(n)]
        ypos = [random.randint(
            2, self.background.get_height() - 2) for _ in xrange(n)]
        return zip(xpos, ypos)
