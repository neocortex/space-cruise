import pygame
import sys

from display_text import DisplayText
from end import draw_end
from entities import Bullet, Enemy1, Enemy2, Explosion, Rock, Spaceship, Star
from title import draw_title, title_stars


class SpaceCruise(object):

    def __init__(self, screen, background, clock):
        self.screen = screen
        self.background = background
        self.clock = clock

    def title_loop(self):
        """ The title screen loop. """
        # Start music
        self.play_music('title')
        # Get title screen stars
        stars = title_stars(self.background)
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
                        self.stop_music()
                        running = False
                        self.game_loop()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
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
                draw_title(self.screen, self.background, stars, draw_msg)

    def play_music(self, part):
        tracks = {
            'title': 'sounds/Hudsons Adventure Island - NES - Title Theme.mp3',
            'game': 'sounds/Lagoon - SNES - Phantom Hill.mp3',
            'end': 'sounds/Hudsons Adventure Island - NES - Title Theme.mp3'}
        pygame.mixer.music.load(tracks[part])
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def init_game(self):
        # Start music
        self.play_music('game')
        # Init entities
        self.ship = Spaceship(self.background)
        self.bullets = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        for s in xrange(self.background.get_height() / 10):
            self.stars.add(Star(self.background, s * 10))
        self.enemies1 = pygame.sprite.Group()
        self.enemies1.add(Enemy1(self.background))
        self.enemies2 = pygame.sprite.Group()
        self.enemies2.add(Enemy2(self.background))
        self.rocks = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.display_txt = DisplayText(self.background)
        # Init some variables
        self.enemy_timer = 2000
        self.dead = False
        self.auslauf = 40
        self.move = 'center'
        self.running = True

    def preparing_end(self):
        self.clock.tick(30)
        self.auslauf -= 1
        self.explosions.update()
        self.background.fill((0, 0, 0))
        self.stars.add(Star(self.background))
        self.stars.update()
        self.enemies1.update()
        self.enemies2.update()
        self.rocks.update()
        if not self.auslauf:
            self.running = False
            self.end_loop()

    def game_loop(self):
        """ The game loop. """
        # Init main loop
        self.init_game()
        # Loop
        while self.running:
            if self.dead:
                self.preparing_end()
            else:
                self.clock.tick(30)
                # Process keyboard input
                for event in pygame.event.get():
                    key = pygame.key.get_pressed()
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.move = 'left'
                        elif event.key == pygame.K_RIGHT:
                            self.move = 'right'
                        elif event.key == pygame.K_UP:
                            self.move = 'up'
                        elif event.key == pygame.K_DOWN:
                            self.move = 'down'
                        elif event.key == pygame.K_ESCAPE:
                            sys.exit()
                        if event.key == pygame.K_SPACE:
                            self.bullets.add(Bullet(self.ship, self.background))
                    elif (event.type == pygame.KEYUP and
                          (not key[pygame.K_LEFT] and not key[pygame.K_DOWN]
                           and not key[pygame.K_UP]
                           and not key[pygame.K_RIGHT])):
                        self.move = 'center'
                    elif (event.type == pygame.KEYUP and
                          (not key[pygame.K_LEFT] and not key[pygame.K_DOWN]
                           and not key[pygame.K_UP] and key[pygame.K_RIGHT])):
                        self.move = 'right'
                    elif (event.type == pygame.KEYUP and
                          (key[pygame.K_LEFT] and not key[pygame.K_DOWN]
                           and not key[pygame.K_UP]
                           and not key[pygame.K_RIGHT])):
                        self.move = 'left'
                    elif (event.type == pygame.KEYUP and
                          (not key[pygame.K_LEFT] and not key[pygame.K_DOWN]
                           and key[pygame.K_UP] and not key[pygame.K_RIGHT])):
                        self.move = 'up'
                    elif (event.type == pygame.KEYUP and
                          (not key[pygame.K_LEFT] and key[pygame.K_DOWN]
                           and not key[pygame.K_UP]
                           and not key[pygame.K_RIGHT])):
                        self.move = 'down'
                # Update entities
                self.background.fill((0, 0, 0))
                self.ship.update(self.move)
                self.bullets.update()
                self.stars.add(Star(self.background))
                self.stars.update()
                self.enemy_timer -= self.clock.get_time()
                if self.enemy_timer < 0:
                    self.enemies1.add(Enemy1(self.background))
                    self.enemies2.add(Enemy2(self.background))
                    self.rocks.add(Rock(self.background))
                    self.enemy_timer = 2000
                self.enemies1.update()
                self.enemies2.update()
                self.rocks.update()
                # Check collisions
                self.collisions = pygame.sprite.groupcollide(
                    self.enemies1, self.bullets, 1, 1)
                self.collisions.update(pygame.sprite.groupcollide(
                    self.enemies2, self.bullets, 1, 1))
                for collision in self.collisions.keys():
                    self.explosions.add(
                        Explosion(self.background, collision.rect))
                    self.display_txt.add_kill()
                collide = pygame.sprite.spritecollide(
                    self.ship, self.rocks, False)
                collide2 = pygame.sprite.spritecollide(
                    self.ship, self.enemies1, False)
                collide3 = pygame.sprite.spritecollide(
                    self.ship, self.enemies2, False)
                if collide or collide2 or collide3:
                    self.explosions.add(
                        Explosion(self.background, self.ship.rect))
                    self.ship.kill()
                    self.dead = True
                self.explosions.update()
                self.display_txt.update()
            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

    def end_loop(self):
        """ The game over loop. """
        self.stars = title_stars(self.background)
        self.play_music('end')
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        self.stop_music()
                        running = False
                        self.game_loop()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            self.clock.tick(100)
            draw_end(self.screen, self.background, self.stars, self.display_txt)


def main():
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
    # Create game object
    space_cruise = SpaceCruise(screen, background, clock)
    space_cruise.title_loop()

if __name__ == "__main__":
    main()
