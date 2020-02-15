import pygame
import math
from general_classes import DotIndicator

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
        self.impulse_angle_rad_2 = 0
        self.x_impulse = 0
        self.y_impulse = 0

        self.max_turn_angle = 360 / (mass**10)

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

        angle_rad = math.atan2(self.rel_y, self.rel_x)
        angle_deg = math.degrees(angle_rad)
        if angle_deg > 0:
            self.impulse_angle_rad_2 = angle_deg + 90
        elif 0 > angle_deg > -90:
            self.impulse_angle_rad_2 = 90 + angle_deg
        elif angle_deg < -90:
            self.impulse_angle_rad_2 = 360 + (angle_deg + 90)

        self.impulse_angle_rad_2 = math.radians(self.impulse_angle_rad_2)

        if self.angle_deg - math.degrees(self.impulse_angle_rad_2) > self.max_turn_angle:
            self.impulse_angle_rad -= math.radians(self.angle_deg - math.degrees(self.impulse_angle_rad_2) - self.max_turn_angle)

    def _split_impulse(self, angle_rad, impulse) -> list:
        full_angle = math.degrees(angle_rad)
        if 0 < full_angle < 90:
            angle = math.radians(full_angle)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            x = abs(sin_a * impulse)
            y = -abs(cos_a * impulse)
        elif 90 < full_angle < 180:
            angle = math.radians(full_angle - 90)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            x = abs(cos_a * impulse)
            y = abs(sin_a * impulse)
        elif 180 < full_angle < 270:
            angle = math.radians(full_angle - 180)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            x = -abs(sin_a * impulse)
            y = abs(cos_a * impulse)
        elif 180 < full_angle < 360:
            angle = math.radians(full_angle - 270)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            x = -abs(cos_a * impulse)
            y = -abs(sin_a * impulse)
        return [x, y]

    def calculate_absolute_angle(self, x_vel, y_vel) -> list:
        if x_vel == 0 and y_vel == 0:
            pass
            print('XXXXXXXXXXXX')
        elif x_vel == 0 and y_vel > 0:
            angle_deg = 0
        elif x_vel == 0 and y_vel < 0:
            angle_deg = 180
        elif x_vel > 0 and y_vel == 0:
            angle_deg = 90
        elif x_vel < 0 and y_vel == 0:
            angle_deg = 270
        else:
            angle_rad = math.atan2(y_vel, x_vel)
            angle_deg = math.degrees(angle_rad)
            if angle_deg > 0:
                angle_deg = angle_deg + 90
            elif 0 > angle_deg > -90:
                angle_deg = 90 + angle_deg
            elif angle_deg < -90:
                angle_deg = 360 + (angle_deg + 90)

        angle_rad = math.radians(angle_deg)
        return [angle_deg, angle_rad]

    def calculate_next_move(self):
        self._get_distance_to_target()
        self._get_impulse_angle()
        self.x_impulse, self.y_impulse = self._split_impulse(self.impulse_angle_rad_2, self.impulse)

    def end_movement(self):
        self.x = self.target_x
        self.y = self.target_y
        self.x_vel = 0
        self.y_vel = 0

    def move(self):
        self.previous_x_vel = self.x_vel
        self.previous_y_vel = self.y_vel

        # if self.distance_to_target <= (self.impulse * self.current_vel_level * 3) and not self.stopping:
        #     if self.x_vel == 0 and self.y_vel == 0:  # Don't do anything if not moving
        #         print('decelerating - passing')
        #         pass
        #     else:
        #         print('decelerating - action')
        #         self.decelerating_vel = self.vel * (1/7)
        #         cos_a = math.cos(self.impulse_angle_rad)
        #         sin_a = math.sin(self.impulse_angle_rad)
        #         self.x_dec_vel = abs(cos_a * self.decelerating_vel)
        #         self.y_dec_vel = abs(sin_a * self.decelerating_vel)
        #
        #         if self.x_impulse > 0:
        #             self.x_dec_vel *= -1
        #         if self.y_impulse > 0:
        #             self.y_dec_vel *= -1
        #
        #         self.stopping = True

        if not self.stopping:
            print('Normal move')
            self.x_vel += self.x_impulse
            self.y_vel += self.y_impulse

            self.vel = math.sqrt(self.x_vel**2 + self.y_vel**2)
            self.current_vel_level = round(self.vel / self.impulse)

            if self.distance_to_target <= self.vel:
                self.end_movement()
            else:
                if self.vel > self.max_vel:
                    print('max Velocity ')
                    angle_deg, angle_rad = self.calculate_absolute_angle(self.x_vel, self.y_vel)
                    self.max_x_vel, self.max_y_vel = self._split_impulse(angle_rad, self.max_vel)

                    self.x_vel = self.max_x_vel
                    self.y_vel = self.max_y_vel

                self.x += self.x_vel
                self.y += self.y_vel
        else:
            if self.distance_to_target > self.vel:
                print('stopping process continues')
                self.x_vel += self.x_dec_vel
                self.y_vel += self.y_dec_vel

                self.x += self.x_vel
                self.y += self.y_vel
            else:
                self.end_movement()

        # calculate ship angles for the upcoming move
        if self.x_vel == 0 and self.y_vel == 0:
            self.angle_deg, self.angle_rad = self.calculate_absolute_angle(self.previous_x_vel, self.previous_y_vel)
        else:
            self.angle_deg, self.angle_rad = self.calculate_absolute_angle(self.x_vel, self.y_vel)

        self.image_angle_deg = self.angle_deg

    def draw(self):
        # pygame.draw.rect(self.screen, color1, (self.x-5, self.y-5, 10, 10))

        self.image = pygame.transform.rotate(self.original_image, -self.image_angle_deg)
        self.rect = self.image.get_rect()  # replace old rect with new one
        self.rect.center = (self.x, self.y)  # set the center of the new rect to the same place as old
        self.screen.blit(self.image, self.rect)

    def show_object_values(self):
        print(f'       X: {self.x}, Y: {self.y}')
        print(f'Target X: {self.target_x}, Y: {self.target_y}')
        print(f'Impulse X: {self.x_impulse}, Y: {self.y_impulse}')
        print('')
        print(f'Impulse Angle: {math.degrees(self.impulse_angle_rad)}')
        print(f'Impulse Angle 2: {math.degrees(self.impulse_angle_rad_2)}')
        print(f'Ship Angle: {self.angle_deg}')
        print(f'Max turn angle: {self.max_turn_angle}')
        print('')
        print(f'Velocity: {self.vel}')
        print(f'velocity X: {self.x_vel}, Y:{self.y_vel}')
        print('')
        print(f'Maximum turn angle: {self.max_turn_angle}')


