import pygame


class spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def get_size(self):
        return self.sheet.get_size()

    def imgat(self, rect, colorkey=None):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def imgsat(self, rects, colorkey=None):
        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect, colorkey))
        return imgs
