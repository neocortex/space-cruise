import random
import sys

import pygame
import spritesheet


# Color: black
BLACK = (0, 0, 0)


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
        self.rect = pygame.Rect(self.pos_x, self.pos_y,
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
        self.speed = 1.5+random.random()

    def update(self):
        self.pos_y += self.speed
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


def draw_title(screen, background, stars, draw_msg=True):
    """ Draw the screen title. Includes the title pixel image, the background
        stars, and the enter message.

    """
    background.fill(BLACK)
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


def main_loop(screen, background, clock):
    pygame.mixer.music.load(
        'sounds/Hudsons Adventure Island - NES - Title Theme.mp3')
    pygame.mixer.music.play(-1)
    running = True
    stars = title_stars(background)
    draw_msg = True
    draw_msg_time = 500
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    running = False
                    game_loop(screen, background, clock)
                elif event.key == pygame.K_ESCAPE:
                    running = False
        time_passed = clock.tick(100)
        if draw_msg_time >= 1000:
            draw_msg = True
        elif draw_msg_time <= 0:
            draw_msg = False
        if draw_msg:
            draw_msg_time -= time_passed*2
        else:
            draw_msg_time += time_passed*2
        if running:
            draw_title(screen, background, stars, draw_msg)


def draw_end(screen, background, stars):
    """ Draw the game over screen. """
    background.fill(BLACK)
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


def game_over(screen, background, clock):
    """ The game over loop. """
    stars = title_stars(background)
    pygame.mixer.music.load(
        'sounds/Hudsons Adventure Island - NES - Title Theme.mp3')
    pygame.mixer.music.play(-1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    running = False
                    game_loop(screen, background, clock)
                elif event.key == pygame.K_ESCAPE:
                    running = False
        clock.tick(100)
        draw_end(screen, background, stars)


def game_loop(screen, background, clock):
    """ The game loop. """
    pygame.mixer.music.load('sounds/Lagoon - SNES - Phantom Hill.mp3')
    pygame.mixer.music.play(-1)
    ship = Spaceship(background)
    bullets = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    for s in xrange(background.get_height() / 10):
        stars.add(Star(background, s * 10))
    ufos = pygame.sprite.Group()
    move = 'center'
    ufotimer = 2000
    enemies1 = pygame.sprite.Group()
    enemies1.add(Enemy1(background))
    enemies2 = pygame.sprite.Group()
    enemies2.add(Enemy2(background))
    rocks = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    dead = False
    auslauf = 40

    running = True
    while running:
        if dead:
            clock.tick(30)
            auslauf -= 1
            explosions.update()
            background.fill(BLACK)
            stars.add(Star(background))
            stars.update()
            enemies1.update()
            enemies2.update()
            rocks.update()
            if not auslauf:
                running = False
                game_over(screen, background, clock)
        else:
            clock.tick(30)
            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move = 'left'
                    elif event.key == pygame.K_RIGHT:
                        move = 'right'
                    elif event.key == pygame.K_UP:
                        move = 'up'
                    elif event.key == pygame.K_DOWN:
                        move = 'down'
                    elif event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        bullets.add(Bullet(ship, background))
                elif (event.type == pygame.KEYUP and
                     (not key[pygame.K_LEFT] and not key[pygame.K_DOWN]
                      and not key[pygame.K_UP] and not key[pygame.K_RIGHT])):
                    move = 'center'
                elif (event.type == pygame.KEYUP and
                     (not key[pygame.K_LEFT] and not key[pygame.K_DOWN]
                      and not key[pygame.K_UP] and key[pygame.K_RIGHT])):
                    move = 'right'
                elif (event.type == pygame.KEYUP and
                     (key[pygame.K_LEFT] and not key[pygame.K_DOWN]
                      and not key[pygame.K_UP] and not key[pygame.K_RIGHT])):
                    move = 'left'
                elif (event.type == pygame.KEYUP and
                     (not key[pygame.K_LEFT] and not key[pygame.K_DOWN]
                      and key[pygame.K_UP] and not key[pygame.K_RIGHT])):
                    move = 'up'
                elif (event.type == pygame.KEYUP and
                     (not key[pygame.K_LEFT] and key[pygame.K_DOWN]
                      and not key[pygame.K_UP] and not key[pygame.K_RIGHT])):
                    move = 'down'

            background.fill(BLACK)
            ship.update(move)
            bullets.update()
            stars.add(Star(background))
            stars.update()
            ufotimer -= clock.get_time()
            if ufotimer < 0:
                enemies1.add(Enemy1(background))
                enemies2.add(Enemy2(background))
                rocks.add(Rock(background))
                ufotimer = 2000
            ufos.update()
            enemies1.update()
            enemies2.update()
            rocks.update()
            collisions = pygame.sprite.groupcollide(ufos, bullets, 1, 1)
            collisions.update(pygame.sprite.groupcollide(
                              enemies1, bullets, 1, 1))
            collisions.update(pygame.sprite.groupcollide(
                              enemies2, bullets, 1, 1))
            for collision in collisions.keys():
                explosions.add(Explosion(background, collision.rect))
            collide = pygame.sprite.spritecollide(ship, rocks, False)
            collide2 = pygame.sprite.spritecollide(ship, enemies1, False)
            collide3 = pygame.sprite.spritecollide(ship, enemies2, False)
            if collide or collide2 or collide3:
                explosions.add(Explosion(background, ship.rect))
                ship.kill()
                dead = True
            explosions.update()
        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    # Init Pygame
    pygame.init()
    # Set screen
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Space Cruise')
    # Set time
    clock = pygame.time.Clock()
    # Set background
    background = pygame.Surface(screen.get_size())
    # Keys that are held down will generate multiple KEYDOWN events
    # pygame.key.set_repeat(1,30)
    main_loop(screen, background, clock)
