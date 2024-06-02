import pygame
import os
import settings
from os.path import join
from classes.player import Player
from classes.meteor import Meteor
from classes.star import Star
from classes.explosion import Explosion

#general setup
pygame.init()
display_surface = pygame.display.set_mode((settings.window_width, settings.window_height))
pygame.display.set_caption(settings.title)
pygame.display.set_icon(pygame.image.load(os.path.os.path.join('space shooter', 'images','player.png')))
clock = pygame.time.Clock()
running = True

#imports
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

#load images of recurring items here so they only need to get loaded once
star_image = pygame.image.load(os.path.join('space shooter', 'images','star.png')).convert_alpha()
meteor_image = pygame.image.load(os.path.join('space shooter', 'images','meteor.png')).convert_alpha()

#importing multiple images for an animation
explosion_frames = [pygame.image.load(join('space shooter', 'images', 'explosion',
                                            f'{i}.png')).convert_alpha() for i in range(21)]
#font
font = pygame.font.Font(os.path.join('space shooter', 'images','Oxanium-bold.ttf'), 20)
font_gameover = pygame.font.Font(os.path.join('space shooter', 'images','Oxanium-bold.ttf'), 100)

#sound
game_sound = pygame.mixer.Sound(join('space shooter', 'audio','game_music.wav'))
game_sound.set_volume(0.2)
game_sound.play(-1)

#populate starfield background
for i in range(20):
    Star(all_sprites, star_image)
player = Player((all_sprites,laser_sprites))


#custom meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 1000)


def collisions():
    #player - meteor collision
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        display_surface.blit(font_gameover.render(f"GAME OVER", True, (255, 255, 255)), (settings.window_width/2, settings.window_height/2))
        display_surface.blit(font.render(f"Final Score {player.score}", True, (255, 255, 255)), (settings.window_width/2, (settings.window_height/2)+150))

    #laser - meteor collision
    for laser in laser_sprites:
        collision_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True, pygame.sprite.collide_mask)
        if collision_sprites:
            player.update_score(10)
            laser.kill()
            Explosion(all_sprites, explosion_frames, laser.rect.midtop)

# main game loop
while running:

    dt = clock.tick() / 1000 

    #event loop
    for event in pygame.event.get():
        #on quit event, set running to false and close the while loop
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor((all_sprites, meteor_sprites), meteor_image)

    #draw the game
    all_sprites.update(dt)
    #do all the collision checks
    collisions()

    display_surface.fill((0, 0, 10))
    all_sprites.draw(display_surface)
    display_surface.blit(font.render(f"Score: {player.score}", True, (255, 0, 0)), (10, 10))

    pygame.display.update()
    
#close game            
pygame.quit()
