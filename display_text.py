import pygame


WHITE = (255, 255, 255)


class DisplayText(object):
    """ The display for the time and the kills count. """

    def __init__(self, background):
        self.background = background
        self.frame_count = 0
        self.frame_rate = 30
        self.kills = 0
        self.text_rect = pygame.draw.rect(
            self.background, WHITE, (1, 1, 90, 50), 2)
        self.font = pygame.font.SysFont(u'tlwgtypewriter', 15)
        self.time_str = self.font.render(
            'Time  {:2}'.format(0), True, WHITE)
        self.time_rect = self.time_str.get_rect()
        self.time_rect.centery = (
            self.text_rect.centery - self.text_rect.height / 4)
        self.time_rect.centerx = self.text_rect.centerx
        self.kills_str = self.font.render(
            'Kills {:2}'.format(self.kills), True, WHITE)
        self.kills_rect = self.kills_str.get_rect()
        self.kills_rect.centery = (
            self.text_rect.centery + self.text_rect.height / 4)
        self.kills_rect.left = self.time_rect.left

    def add_kill(self):
        self.kills += 1

    def update(self):
        self.frame_count += 1
        total_time = self.frame_count // self.frame_rate
        seconds = total_time % 60
        self.time_str = self.font.render(
            'Time  {:2}'.format(seconds), True, WHITE)
        self.kills_str = self.font.render(
            'Kills {:2}'.format(self.kills), True, WHITE)
        self.background.blit(self.time_str, self.time_rect)
        self.background.blit(self.kills_str, self.kills_rect)
        pygame.draw.rect(self.background, WHITE, self.text_rect, 2)
