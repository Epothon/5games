import settings
import pygame
from os.path import join
from classes.laser import Laser

class Player(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)
        #load the sprite groups to be able to fire lasers etc 
        self.groups = groups
        #loading images of player and laser images (to load only once)
        self.image = pygame.image.load(join('space shooter', 'images', 'player.png')).convert_alpha()
        self.laser_image = pygame.image.load(join('space shooter', 'images','laser.png')).convert_alpha()

        #sound
        self.laser_sound = pygame.mixer.Sound(join('space shooter', 'audio','laser.wav'))
        self.laser_sound.set_volume(0.5)


        #spawn in the center of the screen
        self.rect = self.image.get_frect(center=((settings.window_width/2),(settings.window_height/2)))
        self.speed = 300
        self.direction = pygame.math.Vector2(0, 0)
        self.score = 0

        #laser cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.shoot_cooldown_duration = 400

    #doing the fire check by comparing timer and cooldown
    def check_fire_possible(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time > self.shoot_cooldown_duration:
                self.can_shoot = True
                Laser(self.groups, self.laser_image, self.rect.midtop, self.speed)
                self.update_score(-1)
                self.laser_sound.play()

    def player_kill(self):
        print("player killed")
        self.kill()

    def update_score(self, update_score):
        self.score += update_score

    def score(self):
        return f"{self.score}"

    def update(self, dt):
        #player movement
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += (self.direction * self.speed * dt)

        #boundary check
        if self.rect.left <= 0 or self.rect.right >= settings.window_width:
           self.direction.x = 0
        if self.rect.top <= 0 or self.rect.bottom >= settings.window_height:
            self.direction.y = 0
        #boundry check and set back if exceeding to prevent movement exceeding fps            
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.right >= settings.window_width:
            self.rect.right = settings.window_width  
        if self.rect.bottom >= settings.window_height:
            self.rect.bottom = settings.window_height

        #laser shooting on spacebar
        if keys[pygame.K_SPACE] & self.can_shoot:
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks() #get current time to use in delaytimer
        
        #check if it is possible to fire laser
        self.check_fire_possible()
