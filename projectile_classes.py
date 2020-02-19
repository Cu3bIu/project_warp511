import pygame
import math


class Projectile(pygame.Rect):
    def __init__(self, x, y, target_x, target_y):
        pygame.Rect.__init__(self, x, y, 5, 5)

        # Coordinates:
        # -bullet
        self.x = x
        self.y = y
        # -ship (at the moment of a shot)
        self.ship_x = x
        self.ship_y = y
        # -target
        self.target_x = target_x
        self.target_y = target_y

        self.speed = 15  # px per screen
        self.color = (255, 0, 0)

        # counting Step (=speed) coordinates needed to move to target in one tick
        self.step_x_initial = (self.target_x - self.x) * self.speed \
                      / math.sqrt((self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2)
        self.step_y_initial = (self.target_y - self.y) * self.speed \
                      / math.sqrt((self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2)

    # making one Step move to target
    def move_step(self):

        # if bullet went through target point it still should continue moving in this direction
        if abs(self.x-self.ship_x) >= abs(self.target_x-self.ship_x):
            self.step_x = self.step_x_initial
            self.step_y = self.step_y_initial

        # recounting Step coordinates to compensate rounding error
        else:
            self.step_x = (self.target_x - self.x) * self.speed \
                          / math.sqrt((self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2)
            self.step_y = (self.target_y - self.y) * self.speed \
                          / math.sqrt((self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2)

        # moving bullet for one Step
        self.x += self.step_x
        self.y += self.step_y

    # drawing bullet on the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self)
