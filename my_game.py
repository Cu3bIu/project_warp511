import pygame
import sys
import time

from entity_classes import Entity
from projectile_classes import Projectile

# setting the size of the screen
screen_x = 1000
screen_y = 500
screen = pygame.display.set_mode((screen_x, screen_y))

# setting the game name
pygame.display.set_caption('my first game')

red = (255, 0, 0)
black = (0, 0, 0)

elements_list = []
move_list = []
bullets_list = []

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

        # click on right mouse button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            print("----click2----")
            mouse2x, mouse2y = pygame.mouse.get_pos()  # target position
            if mouse2x != player.x and mouse2y != player.y:
                print((player.x, player.y), (mouse2x, mouse2y))
                bullets_list.append(Projectile(player.x, player.y, mouse2x, mouse2y))

    for bullet in bullets_list:
        bullet.move_step()
        print(bullet, bullet.step_x, bullet.step_y)
        if (screen_x < bullet.x or bullet.x < 0
                or screen_y < bullet.y or bullet.y < 0):
            bullets_list.remove(bullet)
        bullet.draw(screen)

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
