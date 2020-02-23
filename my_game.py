import pygame
import sys
import time

from entity_classes import Entity
from projectile_classes import Projectile

# setting the size of the screen
screen_x = 1200
screen_y = 700
screen = pygame.display.set_mode((screen_x, screen_y))

# setting the game name
pygame.display.set_caption('my first game')

red = (255, 0, 0)
black = (0, 0, 0)

elements_list = []
move_list = []
bullets = pygame.sprite.Group()    # Group for bullets on screen

mass = 20

player = Entity(300, 150, 30, 30, mass, 10, (255, 0, 0), screen, 'res/ship/player100x100.png')
player.draw()

pygame.display.update()

# adding elements that are currently active
elements_list.append(player)

background_image = pygame.image.load('res/background/star-sky.png').convert()


def add_to_move_list(x):
    try:
        move_list.index(x)
    except ValueError:
        move_list.append(x)


while True:
    screen.blit(background_image, [0, 0])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("----click----")
            mx, my = pygame.mouse.get_pos()
            player.move_to(mx, my)
            add_to_move_list(player)

        # click on right mouse button - fire
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            print("----click2----")
            projectile = Projectile(player.x, player.y, pygame.mouse.get_pos())
            print(projectile.angle)
            bullets.add(projectile)

    # move all bullets for one step
    bullets.update()
    for bullet in bullets:
        print(bullet.pos, bullet.target)
        if not screen.get_rect().contains(bullet.rect):
            bullet.remove(bullets)

    # draw all bullets
    bullets.draw(screen)

    for element in move_list:
        if element.need_to_move():
            element.calculate_next_move()
            element.move()
            # element.show_object_values()
        element.draw()

    # print(len(move_list))
    pygame.display.update()
    print('------------------NEXT TICK-----------------')
    time.sleep(0.1)
