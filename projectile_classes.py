import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        pygame.sprite.Sprite.__init__(self)

        # these parameters should be moved to subclasses
        self.speed = 8  # px per tick
        self.image = pygame.image.load('res\projectile\projectile.png').convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.center = (x, y)

        self.pos = pygame.Vector2(self.rect.center)  # bullet position vector
        self.target = pygame.Vector2(target_pos)  # target position vector
        self.move = self.target - self.pos  # vector between bullet and target
        move_length = self.move.length()
        self.angle = self.move.angle_to(pygame.Vector2(1, 0))  # angle to target

        self.rotate(self.angle)

        if move_length < self.speed:
            self.pos = self.target
        elif move_length != 0:
            self.move.normalize_ip()
            self.move = self.move * self.speed

    def rotate(self, angle):
        """rotate an image"""
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.pos += self.move
        self.rect.center = list(int(v) for v in self.pos)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('res\ship\player100x100 - bad.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += 3
        if self.rect.left > 1200:
            self.rect.right = 0
