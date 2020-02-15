import pygame
import math

class DotIndicator:
    def __init__(self, screen):
        self.color = (255, 0, 0)
        self.screen = screen

    def draw(self, x, y):
        pygame.draw.rect(self.screen, self.color, (x, y, 5, 5))

    def show(self):
        pass