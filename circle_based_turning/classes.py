import pygame
import math
import numpy as np

from sympy.solvers import solve
from sympy import Symbol

color1 = (20, 100, 55)
color2 = (100, 150, 2)


class Entity:
    def __init__(self, x, y, height, width, mass, power, color, screen, image_path):
        self.indicator = DotIndicator(screen)
        self.indicate = True

        self.x = x
        self.y = y
        self.height = height
        self.width = width

        self.mass = mass
        self.power = power

        self.vel = 0
        self.x_vel = 0
        self.y_vel = 0
        self.previous_x_vel = 0
        self.previous_y_vel = 0

        self.max_vel_multiplier = 7
        self.max_vel = (power / mass) * self.max_vel_multiplier
        self.max_x_vel = 0
        self.max_y_vel = 0

        self.impulse = power / mass
        self.impulse_angle_rad = 0
        self.x_impulse = 0
        self.y_impulse = 0

        self.current_vel_level = 0  # How many steps it will take to decelerate
        self.vel_ticks_from_target = 0  # distance from x,y to target_x,target_y

        self.target_x = x
        self.target_y = y

        self.stopping = False
        self.decelerating_vel = 0
        self.x_dec_vel = 0
        self.y_dec_vel = 0

        self.rel_x = 0
        self.rel_y = 0
        self.distance_to_target = 0

        self.screen = screen
        self.color = color

        self.angle_deg = 0  # 0 degrees is pointing vertically UP
        self.angle_rad = 0

        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image
        self.image_angle_deg = False  # changed to numeric value after the first move()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.bank_angle_deg = 30

        self.turn_radius_deg = 0
        self.turn_radius_angle_deg = 0
        self.turn_radius_len = 100
        self.turn_circle_center_x = 0
        self.turn_circle_center_y = 0

    def move_to(self, x, y):
        self.target_x = x
        self.target_y = y
        self.stopping = False

    def need_to_move(self):
        return self.x != self.target_x and self.y != self.target_y

    def _get_distance_to_target(self):
        self.rel_x = self.target_x - self.x
        self.rel_y = self.target_y - self.y
        self.distance_to_target = math.sqrt((self.rel_x**2 + self.rel_y**2))

    def _get_impulse_angle(self):
        tan_a = self.rel_y / self.rel_x
        self.impulse_angle_rad = math.atan(tan_a)

    def _split_impulse(self):
        cos_a = math.cos(self.impulse_angle_rad)
        sin_a = math.sin(self.impulse_angle_rad)

        self.x_impulse = abs(cos_a * self.impulse)
        self.y_impulse = abs(sin_a * self.impulse)

        self.max_x_vel = abs(cos_a * self.max_vel)
        self.max_y_vel = abs(sin_a * self.max_vel)

        if (self.target_x - self.x) < 0:
            self.x_impulse *= -1
            self.max_x_vel *= -1
        if (self.target_y - self.y) < 0:
            self.y_impulse *= -1
            self.max_y_vel *= -1

    def calculate_absolute_angle(self):
        # saving the previous velocity
        self.previous_x_vel = self.x_vel
        self.previous_y_vel = self.y_vel

        if self.x_vel == 0 and self.y_vel == 0:
            pass
            print('XXXXXXXXXXXX')
        elif self.x_vel == 0 and self.y_vel > 0:
            self.angle_deg = 0
        elif self.x_vel == 0 and self.y_vel < 0:
            self.angle_deg = 180
        elif self.x_vel > 0 and self.y_vel == 0:
            self.angle_deg = 90
        elif self.x_vel < 0 and self.y_vel == 0:
            self.angle_deg = 270
        else:
            angle_rad = math.atan2(self.y_vel, self.x_vel)
            angle_deg = math.degrees(angle_rad)
            if angle_deg > 0:
                self.angle_deg = angle_deg + 90
            elif 0 > angle_deg > -90:
                self.angle_deg = 90 + angle_deg
            elif angle_deg < -90:
                self.angle_deg = 360 + (angle_deg + 90)

        self.angle_rad = math.radians(self.angle_deg)
        self.image_angle_deg = self.angle_deg

    def calculate_turn_circle_center(self):
        if self.x_vel > 0 and self.y_vel < 0:
            a = math.cos(self.angle_rad) * self.turn_radius_len
            b = math.sin(self.angle_rad) * self.turn_radius_len
            self.turn_circle_center_x = self.x + a
            self.turn_circle_center_y = self.y + b

        elif self.x_vel > 0 and self.y_vel > 0:
            a = math.cos(self.angle_rad + math.radians(-90)) * self.turn_radius_len
            b = math.sin(self.angle_rad + math.radians(-90)) * self.turn_radius_len
            self.turn_circle_center_x = self.x - b
            self.turn_circle_center_y = self.y + a

        elif self.x_vel < 0 and self.y_vel > 0:
            a = math.cos(self.angle_rad + math.radians(-180)) * self.turn_radius_len
            b = math.sin(self.angle_rad + math.radians(-180)) * self.turn_radius_len
            self.turn_circle_center_x = self.x - a
            self.turn_circle_center_y = self.y - b

        elif self.x_vel < 0 and self.y_vel < 0:
            a = math.cos(self.angle_rad + math.radians(-270)) * self.turn_radius_len
            b = math.sin(self.angle_rad + math.radians(-270)) * self.turn_radius_len
            self.turn_circle_center_x = self.x + b
            self.turn_circle_center_y = self.y - a

        print(f'Turn Circle center coordinates = {self.turn_circle_center_x}, {self.turn_circle_center_y}')

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
            result_y = solve(x ** 2 - cx * x + cx**2 + y ** 2 - cy * y + cy**2 - r**2, y)
            y_range.append(result_y)

        print(x_range)
        print(y_range)


    def calculate_next_move(self):
        # click event related
        self._get_distance_to_target()
        self._get_impulse_angle()
        self._split_impulse()

    def end_movement(self):
        self.x = self.target_x
        self.y = self.target_y
        self.x_vel = 0
        self.y_vel = 0

    def get_turn_circle(self):
        pass

    def move(self):
        if self.distance_to_target <= (self.impulse * self.current_vel_level * 3) and not self.stopping:
            if self.x_vel == 0 and self.y_vel == 0:  # Don't do anything if not moving
                pass
            else:
                self.decelerating_vel = self.vel * (1/7)
                cos_a = math.cos(self.impulse_angle_rad)
                sin_a = math.sin(self.impulse_angle_rad)
                self.x_dec_vel = abs(cos_a * self.decelerating_vel)
                self.y_dec_vel = abs(sin_a * self.decelerating_vel)

                if self.x_impulse > 0:
                    self.x_dec_vel *= -1
                if self.y_impulse > 0:
                    self.y_dec_vel *= -1

                self.stopping = True

        if not self.stopping:
            self.x_vel += self.x_impulse
            self.y_vel += self.y_impulse

            self.vel = math.sqrt(self.x_vel**2 + self.y_vel**2)
            self.current_vel_level = round(self.vel / self.impulse)

            if self.distance_to_target <= self.vel:
                self.end_movement()
            else:
                if self.vel > self.max_vel:
                    self.x_vel = self.max_x_vel
                    self.y_vel = self.max_y_vel

                self.x += self.x_vel
                self.y += self.y_vel
        else:
            if self.distance_to_target > self.vel:
                self.x_vel += self.x_dec_vel
                self.y_vel += self.y_dec_vel

                self.x += self.x_vel
                self.y += self.y_vel
            else:
                self.end_movement()

        # calculate ship angles for the upcoming move
        self.calculate_absolute_angle()
        self.calculate_turn_circle_center()
        self.calculate_turn_circle_body()

    def draw(self):
        # pygame.draw.rect(self.screen, color1, (self.x-5, self.y-5, 10, 10))

        if self.indicate:
            self.indicator.draw(self.turn_circle_center_x, self.turn_circle_center_y)

        self.image = pygame.transform.rotate(self.original_image, -self.image_angle_deg)
        self.rect = self.image.get_rect()  # replace old rect with new one
        self.rect.center = (self.x, self.y)  # set the center of the new rect to the same place as old
        self.screen.blit(self.image, self.rect)

    def show_object_values(self):
        print(f'       X: {self.x}, Y: {self.y}')
        print(f'Target X: {self.target_x}, Y: {self.target_y}')
        print(f'Angle: {self.angle_deg}')
        print(f'Velocity: {self.vel}')
        print(f'velocity X: {self.x_vel}, Y:{self.y_vel}')
        # print(f'{self.circl}')


class DotIndicator:
    def __init__(self, screen):
        self.color = (255, 0, 0)
        self.screen = screen

    def draw(self, x, y):
        pygame.draw.rect(self.screen, self.color, (x, y, 5, 5))

    def show(self):
        pass


# class Image:
#     def __init(self, screen):
#         self.source_image


class Circle:
    def __init__(self):
        self.r = 0
        self.x = 0
        self.y = 0

    def set_circle(self, radius, x, y):
        self.r = radius
        self.x = x
        self.y = y
