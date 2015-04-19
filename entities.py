import pygame
import random

import spritesheet


class Spaceship(pygame.sprite.Sprite):
    """ The player's spaceship. """
    def __init__(self, background):
        pygame.sprite.Sprite.__init__(self)
        self.background = background
        self.master_img = spritesheet.spritesheet('images/spaceship.png')
        self.sprite_pos = [[42 * x, y, 40, 43]
                           for x in range(3) for y in [43, 89]]
        self.sprite_imgs = self.master_img.imgsat(self.sprite_pos, colorkey=-1)
        self.left_imgs = self.sprite_imgs[0:2]
        self.center_imgs = self.sprite_imgs[2:4]
        self.right_imgs = self.sprite_imgs[4:6]
        self.img_idx = 0
        self.curr_img = self.center_imgs[self.img_idx]
        self.pos_x = self.background.get_rect().centerx
        self.pos_y = self.background.get_rect().bottom-50
        self.speed = 10
        self.rect = pygame.Rect(
            self.pos_x, self.pos_y,
            self.curr_img.get_width(),
            self.curr_img.get_height())

    def update(self, move):
        self.mv_left = 0
        self.mv_right = 0
        self.mv_up = 0
        self.mv_down = 0
        if move == 'center':
            self.curr_img = self.center_imgs[self.img_idx % 2]
        elif move == 'left':
            self.curr_img = self.left_imgs[self.img_idx % 2]
            self.mv_left = -self.speed
        elif move == 'right':
            self.curr_img = self.right_imgs[self.img_idx % 2]
            self.mv_right = self.speed
        elif move == 'up':
            self.curr_img = self.center_imgs[self.img_idx % 2]
            self.mv_up = -self.speed
        elif move == 'down':
            self.curr_img = self.center_imgs[self.img_idx % 2]
            self.mv_down = self.speed
        self.img_idx += 1
        self.pos_x += (self.mv_left + self.mv_right)
        self.pos_y += (self.mv_up + self.mv_down)
        # Update rect for collision detection
        self.rect = self.rect.move(
            (self.mv_left + self.mv_right), (self.mv_up + self.mv_down))
        # Make sure character does not leave screen bounderies
        if self.pos_x > (self.background.get_rect().right - self.rect.width):
            self.pos_x = (self.background.get_rect().right - self.rect.width)
        elif self.pos_x < 0:
            self.pos_x = 0
        elif self.pos_y > (self.background.get_rect().bottom
                           - self.rect.height):
            self.pos_y = (self.background.get_rect().bottom
                          - self.rect.height)
        elif self.pos_y < 0:
            self.pos_y = 0
        self.background.blit(self.curr_img, (self.pos_x, self.pos_y))


class Bullet(pygame.sprite.Sprite):
    """ The bullet of the spaceship. """
    def __init__(self, ship, background):
        pygame.sprite.Sprite.__init__(self)
        self.background = background
        self.img = spritesheet.spritesheet(
            'images/bullet.png').imgat([0, 0, 7, 12], colorkey=-1)
        self.pos_x = ship.pos_x + ship.curr_img.get_rect().centerx - 4
        self.pos_y = ship.pos_y
        self.speed = 10
        self.rect = self.img.get_rect()
        self.sound = pygame.mixer.Sound('sounds/laser.wav')
        self.sound.play()

    def update(self):
        self.pos_y -= self.speed
        if self.pos_y < 0:
            self.kill()
        self.rect = pygame.Rect(
            self.pos_x, self.pos_y, self.rect[2], self.rect[3])
        self.background.blit(self.img, (self.pos_x, self.pos_y))


class Star(pygame.sprite.Sprite):
    """ A star object for the game loop. This is simply a pixel that changes
        randomly changes color and moves from top to bottom of the screen on
        a vertical line.

    """
    def __init__(self, background, pos_y=-1):
        pygame.sprite.Sprite.__init__(self)
        self.background = background
        self.pos_x = random.randint(0, self.background.get_width()-1)
        self.pos_y = pos_y
        self.speed = 10

    def update(self):
        self.pos_y += self.speed
        if self.pos_y > self.background.get_height()-1:
            self.kill()
        self.background.set_at(
            (self.pos_x, self.pos_y),
            (random.randint(0, 255),
             random.randint(0, 255),
             random.randint(0, 255)))


class Enemy1(pygame.sprite.Sprite):
    """ Enemy 1 object class. """
    def __init__(self, background, pos_y=-50):
        pygame.sprite.Sprite.__init__(self)
        self.background = background
        self.master_img = spritesheet.spritesheet('images/enemy1.png')
        self.sprite_pos = [[24 * x, 0, 25, 25] for x in range(4)]
        self.imgs = self.master_img.imgsat(self.sprite_pos, colorkey=-1)
        self.imgs = [pygame.transform.scale(x, (30, 30)) for x in self.imgs]
        self.img_idx = 0
        self.curr_img = self.imgs[self.img_idx]
        self.rect = self.curr_img.get_rect()
        self.pos_x = random.randint(
            0, self.background.get_width() - self.rect.width)
        self.pos_y = pos_y
        self.speed = 1.5 + random.random()
        self.change_dir = True
        self.time_to_change = 10
        self.xplus = False
        self.xminus = False

    def update(self):
        self.pos_y += self.speed
        self.time_to_change -= 1
        if self.time_to_change == 0:
            self.change_dir = not self.change_dir
            self.time_to_change = 10
        if self.change_dir:
            self.change_dir = False
            self.time_to_change = 10
            self.xplus = False
            self.xminus = False
            randn = random.random()
            if randn < .33:
                self.xplus = True
            elif 0.33 <= randn < 0.66:
                self.xminus = True
        if self.xplus:
            self.pos_x += 2
        elif self.xminus:
            self.pos_x -= 2
        self.curr_img = self.imgs[self.img_idx % 4]
        self.img_idx += 1
        if self.pos_y > self.background.get_height()-1:
            self.kill()
        self.rect = pygame.Rect(
            self.pos_x, self.pos_y, self.rect[2], self.rect[3])
        self.background.blit(self.curr_img, (self.pos_x, self.pos_y))


class Enemy2(pygame.sprite.Sprite):
    """ Enemy 2 object class. """
    def __init__(self, background, pos_y=-50):
        pygame.sprite.Sprite.__init__(self)
        self.background = background
        self.master_img = spritesheet.spritesheet('images/enemy2.bmp')
        self.sprite_pos = [[24 * x, 0, 25, 25] for x in range(4)]
        self.imgs = self.master_img.imgsat(self.sprite_pos, colorkey=-1)
        self.imgs = [pygame.transform.scale(x, (30, 30)) for x in self.imgs]
        self.img_idx = 0
        self.curr_img = self.imgs[self.img_idx]
        self.rect = self.curr_img.get_rect()
        self.pos_x = random.randint(
            0, self.background.get_width() - self.rect.width)
        self.pos_y = pos_y
        self.speed = 3 + random.random()

    def update(self):
        self.pos_y += self.speed
        self.curr_img = self.imgs[self.img_idx % 3]
        self.img_idx += 1
        if self.pos_y > self.background.get_height() - 1:
            self.kill()
        self.rect = pygame.Rect(
            self.pos_x, self.pos_y, self.rect[2], self.rect[3])
        self.background.blit(self.curr_img, (self.pos_x, self.pos_y))


class Explosion(pygame.sprite.Sprite):
    """ Explosion object class. """
    def __init__(self, background, rect):
        pygame.sprite.Sprite.__init__(self)
        self.background = background
        self.master_img = spritesheet.spritesheet('images/explosion.gif')
        self.sprite_pos = [[64 * x + 1, 64 * y + 1, 64, 64]
                           for y in range(4) for x in range(3)]
        self.imgs = self.master_img.imgsat(
            self.sprite_pos, colorkey=(0, 0, 0))
        self.img_idx = 0
        self.rect = rect
        self.curr_img = self.imgs[self.img_idx]
        self.sound = pygame.mixer.Sound('sounds/explosion.wav')
        self.sound.play()

    def update(self):
        self.curr_img = pygame.transform.scale(
            self.imgs[self.img_idx], (self.rect.width, self.rect.height))
        self.background.blit(self.curr_img, (self.rect.left, self.rect.top))
        self.img_idx += 1
        if self.img_idx >= len(self.imgs):
            self.kill()


class Rock(pygame.sprite.Sprite):
    """ Rock object class. """
    def __init__(self, background):
        pygame.sprite.Sprite.__init__(self)
        self.background = background
        self.fname = 'images/rock%d.png' % random.randint(1, 6)
        self.sprite = spritesheet.spritesheet(self.fname)
        self.size = self.sprite.get_size()
        self.img = pygame.transform.rotate(
            self.sprite.imgat([0, 0, self.size[0], self.size[1]],
                              colorkey=-1), random.randint(0, 360))
        self.pos_x = random.randint(
            0, self.background.get_width() - self.img.get_width())
        self.pos_y = -50
        self.speed = 1 + random.random()
        self.rect = self.img.get_rect()

    def update(self):
        self.pos_y += self.speed
        self.rect = pygame.Rect(
            self.pos_x, self.pos_y, self.rect[2], self.rect[3])
        self.background.blit(self.img, (self.pos_x, self.pos_y))
        if self.pos_y > self.background.get_height()-1:
            self.kill()
