import pygame
from os.path import join

class Laser(pygame.sprite.Sprite):

    def __init__(self, groups, image, position, speed):
        super().__init__(groups)
        self.image = image
        self.speed = speed
        self.direction = pygame.math.Vector2(0, -1)
        self.rect = self.image.get_frect(midbottom = position)

    def laser_kill(self):
        print("laser killed")
        self.kill()

    def update(self, dt):
        self.rect.center += (self.direction * self.speed * dt)
        if self.rect.bottom < 0:
            self.kill()

