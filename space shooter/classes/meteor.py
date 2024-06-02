import settings
import pygame
import random

class Meteor(pygame.sprite.Sprite):

    def __init__(self, groups, image):
        super().__init__(groups)
        self.original_image = image
        self.image = self.original_image
        self.rotation = 0
        #spawn the meteor along the top edge
        #randomly on y axis
        #and from a different angle on the x axis using uniform
        self.rect = self.image.get_frect(center=(
            random.randint(self.image.get_width(),(settings.window_width-self.image.get_width())),0))
        self.direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), -1)
        #spawnrate is randomized
        self.speed = random.randint(30, 100)
        self.rotation_speed_direction = random.randrange(-50,50)

        
    def update(self, dt):
        #transform
        self.rotation += dt * self.rotation_speed_direction
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

        self.rect.center -= (self.direction * self.speed * dt)
        if self.rect.top > settings.window_height:
            self.kill()
        

