import pygame
import sys

from end import draw_end
from entities import Bullet, Enemy1, Enemy2, Explosion, Rock, Spaceship, Star
from title import draw_title, title_stars


def title_loop(screen, background, clock):
    """ The title screen loop. """
    # Start music
    pygame.mixer.music.load(
        'sounds/Hudsons Adventure Island - NES - Title Theme.mp3')
    pygame.mixer.music.play(-1)
    # Get title screen stars
    stars = title_stars(background)
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
                    pygame.mixer.music.stop()
                    running = False
                    game_loop(screen, background, clock)
                elif event.key == pygame.K_ESCAPE:
                    running = False
        time_passed = clock.tick(100)
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
            draw_title(screen, background, stars, draw_msg)


def end_loop(screen, background, clock):
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
    # Start music
    pygame.mixer.music.load('sounds/Lagoon - SNES - Phantom Hill.mp3')
    pygame.mixer.music.play(-1)
    # Init entities
    ship = Spaceship(background)
    bullets = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    for s in xrange(background.get_height() / 10):
        stars.add(Star(background, s * 10))
    enemies1 = pygame.sprite.Group()
    enemies1.add(Enemy1(background))
    enemies2 = pygame.sprite.Group()
    enemies2.add(Enemy2(background))
    rocks = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    # Init some variables
    enemy_timer = 2000
    dead = False
    auslauf = 40
    move = 'center'
    # Loop
    running = True
    while running:
        if dead:
            clock.tick(30)
            auslauf -= 1
            explosions.update()
            background.fill((0, 0, 0))
            stars.add(Star(background))
            stars.update()
            enemies1.update()
            enemies2.update()
            rocks.update()
            if not auslauf:
                running = False
                end_loop(screen, background, clock)
        else:
            clock.tick(30)
            # Process keyboard input
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
            # Update entities
            background.fill((0, 0, 0))
            ship.update(move)
            bullets.update()
            stars.add(Star(background))
            stars.update()
            enemy_timer -= clock.get_time()
            if enemy_timer < 0:
                enemies1.add(Enemy1(background))
                enemies2.add(Enemy2(background))
                rocks.add(Rock(background))
                enemy_timer = 2000
            enemies1.update()
            enemies2.update()
            rocks.update()
            # Check collisions
            collisions = pygame.sprite.groupcollide(
                enemies1, bullets, 1, 1)
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
    # Keys that are held down will generate multiple KEYDOWN events
    # pygame.key.set_repeat(1,30)
    title_loop(screen, background, clock)


if __name__ == "__main__":
    main()
