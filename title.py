import pygame
import random


class TitleScreen(object):

    def __init__(self, screen, background, clock):
        self.screen = screen
        self.background = background
        self.clock = clock
        self.stars = self.title_stars()
        self.title_img = pygame.image.load('images/cruiser.png')
        self.title_font = pygame.font.SysFont(u'tlwgtypewriter', 20)
        self.start_str = self.title_font.render(
            "PRESS ENTER", True, (255, 255, 255))

    def draw_title(self, draw_msg=True):
        """ Draw the title screen. Includes the title pixel image,
            the background stars, and the enter message.

        """
        self.background.fill((0, 0, 0))
        # Draw stars
        pos = [(0, 0), (-1, 0), (0, -1), (1, 0), (0, 1)]
        for x, y in self.stars:
            for i, j in pos:
                self.background.set_at(
                    (x+i, y+j), (random.randint(0, 255),
                                 random.randint(0, 255),
                                 random.randint(0, 255)))
        # Blit title image
        self.background.blit(self.title_img, (
            (self.background.get_rect().centerx -
             self.title_img.get_width() / 2),
            self.background.get_rect().centery -
            self.title_img.get_height() / 2))
        # Draw enter message
        if draw_msg:
            self.background.blit(self.start_str, (
                self.background.get_rect().centerx -
                self.start_str.get_width() / 2,
                self.background.get_rect().bottom - 80))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def title_stars(self, n=500):
        """ Return random positions for stars on title screen. """
        xpos = [random.randint(
            2, self.background.get_width() - 2) for _ in xrange(n)]
        ypos = [random.randint(
            2, self.background.get_height() - 2) for _ in xrange(n)]
        return zip(xpos, ypos)

    def title_loop(self):
            """ The title screen loop. """
            # Variable to draw 'enter message'
            draw_msg = True
            draw_msg_time = 500
            # Loop
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RETURN:
                            running = False
                            return 'start'
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                            return 'quit'
                time_passed = self.clock.tick(100)
                # Blinking message routine
                if draw_msg_time >= 1000:
                    draw_msg = True
                elif draw_msg_time <= 0:
                    draw_msg = False
                if draw_msg:
                    draw_msg_time -= time_passed*2
                else:
                    draw_msg_time += time_passed*2
                # Draw title screen
                if running:
                    self.draw_title(draw_msg)
