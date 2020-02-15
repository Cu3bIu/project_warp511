import pygame
import sys
import time

from classes import Entity

# seting the size of the screen
screen = pygame.display.set_mode((2000, 1000))

# setting the game name
pygame.display.set_caption('my first game')

red = (255, 0, 0)
black = (0, 0, 0)

elements_list = []
move_list = []

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("----click----")
            mx, my = pygame.mouse.get_pos()
            player.move_to(mx, my)
            add_to_move_list(player)

    for element in move_list:
        if element.need_to_move():
            element.calculate_next_move()
            element.move()
            element.show_object_values()
        element.draw()

    # print(len(move_list))
    pygame.display.update()
    print('------------------NEXT TICK-----------------')
    time.sleep(0.03)
