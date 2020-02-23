import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        pygame.sprite.Sprite.__init__(self)

        # Bullet position:
        self.x = x
        self.y = y

        # these parameters should be moved to subclasses
        self.speed = 8  # px per screen
        self.image = pygame.image.load('res\projectile\projectile.png').convert_alpha()

        self.rect = self.image.get_rect()

        self.pos = pygame.Vector2(self.x, self.y)  # bullet position vector
        self.target = pygame.Vector2(target_pos)  # target position vector
        self.move = self.target - self.pos  # vector between bullet and target
        move_length = self.move.length()
        self.angle = self.move.angle_to(pygame.Vector2(1, 0))  # angle between oX and move Vector

        self.rotate(self.angle)  # rotate image to target

        if move_length < self.speed:
            self.pos = self.target
        elif move_length != 0:
            self.move.normalize_ip()
            self.move = self.move * self.speed

    def rotate(self, angle):
        """rotate an image"""
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()

    def update(self):
        self.pos += self.move
        self.rect.topleft = list(int(v) for v in self.pos)


