import settings
import pygame
import random

class Star(pygame.sprite.Sprite):

    def __init__(self, groups, image):
        super().__init__(groups)
        self.image = image
        # position of the star is chosen randomly between the max screen width and height
        self.rect = self.image.get_frect(
            center=((random.randint(50, settings.window_width)),
                    ((random.randint(50, settings.window_height)))))

