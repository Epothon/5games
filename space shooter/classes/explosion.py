import pygame
from os.path import join

class Explosion(pygame.sprite.Sprite):
    
    def __init__(self, groups, frames, pos):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

        #soundeffect
        explosion_sound = pygame.mixer.Sound(join('space shooter', 'audio','explosion.wav'))
        explosion_sound.play()

    def update(self, dt):
        self.frame_index += 30 * dt
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]