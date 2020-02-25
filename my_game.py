import pygame
import sys

from entity_classes import Entity
from projectile_classes import Projectile, Enemy


pygame.init()
clock = pygame.time.Clock()

# Setting the size of the screen
width, height = (1200, 700)
screen = pygame.display.set_mode((width, height))
fps = 30

# Setting the game name
pygame.display.set_caption('my first game')

# Colors
red = (255, 0, 0)
black = (0, 0, 0)

elements_list = []
move_list = []
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

mass = 20
player = Entity(width/2, height/2, 30, 30, mass, 10, (255, 0, 0), screen, 'res/ship/player100x100.png')
elements_list.append(player)

enemy = Enemy(width/2, 100)
enemy.add(all_sprites)

background_image = pygame.image.load('res/background/star-sky.png').convert()


def add_to_move_list(x):
    try:
        move_list.index(x)
    except ValueError:
        move_list.append(x)

# Game loop
while True:
    clock.tick(fps)

    screen.blit(background_image, [0, 0])

    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Move player
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("----click----")
            mx, my = pygame.mouse.get_pos()
            player.move_to(mx, my)
            add_to_move_list(player)

        # Fire
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            print("----click2----")
            projectile = Projectile(player.x, player.y, pygame.mouse.get_pos())
            print(projectile.angle)
            projectile.add(bullets, all_sprites)

    # Moving and updating
    all_sprites.update()
    bullets.update()

    # Removing bullets those are out of screen
    for bullet in bullets:
        print(bullet.pos, bullet.target)
        if not screen.get_rect().contains(bullet.rect):
            bullet.remove(bullets, all_sprites)

    # Drawing
    all_sprites.draw(screen)

    for element in move_list:
        if element.need_to_move():
            element.calculate_next_move()
            element.move()
            # element.show_object_values()
        element.draw()

    # print(len(move_list))
    pygame.display.update()
    print('------------------NEXT TICK-----------------')

pygame.quit()
