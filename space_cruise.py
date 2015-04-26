import pygame
import sys

from display_text import DisplayText
from end import EndScreen
from entities import Bullet, EnemyOne, EnemyTwo, Explosion, Rock, Spaceship, Star
from title import TitleScreen


class SpaceCruise(object):

    def __init__(self, screen, background, clock):
        self.screen = screen
        self.background = background
        self.clock = clock
        self.display_txt = DisplayText(self.background)
        self.title = TitleScreen(self.screen, self.background, self.clock)
        self.end = EndScreen(
            self.screen, self.background, self.clock, self.display_txt)

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
        self.enemies1.add(EnemyOne(self.background))
        self.enemies2 = pygame.sprite.Group()
        self.enemies2.add(EnemyTwo(self.background))
        self.rocks = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
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
            self.run_end()

    def process_input(self):
        # Process keyboard input
        move_dict = {pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right',
                     pygame.K_UP: 'up', pygame.K_DOWN: 'down'}
        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in move_dict:
                    self.move = move_dict[event.key]
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    self.bullets.add(Bullet(self.ship, self.background))
            elif event.type == pygame.KEYUP:
                if not any(key):
                    self.move = 'center'
                if sum(key) == 1:
                    if key[pygame.K_RIGHT]:
                        self.move = 'right'
                    elif key[pygame.K_LEFT]:
                        self.move = 'left'
                    elif key[pygame.K_UP]:
                        self.move = 'up'
                    elif key[pygame.K_DOWN]:
                        self.move = 'down'

    def update_all(self):
        self.background.fill((0, 0, 0))
        self.ship.update(self.move)
        self.bullets.update()
        self.stars.add(Star(self.background))
        self.stars.update()
        self.enemy_timer -= self.clock.get_time()
        if self.enemy_timer < 0:
            self.enemies1.add(EnemyOne(self.background))
            self.enemies2.add(EnemyTwo(self.background))
            self.rocks.add(Rock(self.background))
            self.enemy_timer = 2000
        self.enemies1.update()
        self.enemies2.update()
        self.rocks.update()

    def check_collisions(self):
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
                self.process_input()
                # Update entities
                self.update_all()
                # Check collisions
                self.check_collisions()
                self.display_txt.update()
            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

    def run_title(self):
        self.play_music('title')
        result = self.title.title_loop()
        if result == 'start':
            self.stop_music()
            self.game_loop()
        elif result == 'quit':
            sys.exit()

    def run_end(self):
        self.play_music('end')
        result = self.end.end_loop()
        if result == 'restart':
            self.stop_music()
            self.display_txt.reset()
            self.game_loop()
        elif result == 'quit':
            sys.exit()


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
    space_cruise.run_title()

if __name__ == "__main__":
    main()
