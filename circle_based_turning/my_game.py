import pygame
import sys
import time

from classes import Entity

from sympy.solvers import solve
from sympy import Symbol
import numpy as np


# seting the size of the screen
screen = pygame.display.set_mode((1024, 768))

# setting the game name
pygame.display.set_caption('my first game')

red = (255, 0, 0)
black = (0, 0, 0)


def calculate_turn_circle_body(self):
    x_limit = [self.turn_circle_center_x - self.turn_radius_len, self.turn_circle_center_x + self.turn_radius_len]
    # y_limit = [self.turn_circle_center_y - self.turn_radius_len, self.turn_circle_center_y + self.turn_radius_len]

    x_range = np.linspace(x_limit[0], x_limit[1], 5)
    y_range = []

    y = Symbol('y')
    cx = 0
    cy = 0
    r = self.turn_radius_len

    for x in x_range:
        result_y = solve(x ** 2 - cx * x + cx ** 2 + y ** 2 - cy * y + cy ** 2 - r ** 2, y)
        y_range.append(result_y)

    print(x_range)
    print(y_range)

# player = Player(0, 0, char_mass, red, screen)
# player.update()

elements_list = []
move_list = []

mass = 5

player = Entity(300, 150, 30, 30, mass, 10, (255, 0, 0), screen, 'res/ship/player100x100.png')
player.draw()
pygame.display.update()

# adding elements that are currently active
elements_list.append(player)


def add_to_move_list(x):
    try:
        move_list.index(x)
    except ValueError:
        move_list.append(x)


while True:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
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
