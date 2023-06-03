import os
import sys

import pygame

pygame.init()

width = 1400
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('hh')

path = os.getcwd()

bird_img = pygame.image.load(os.path.join(path, '../images/base_mid.png')).convert_alpha()
print(path)


# A MASK DOES NOT FOLLOW OBJECT
# A MASK IMAGE IS JUST A IMAGE AND IS LINKED TO NOTHING

# offset --->>> pass in x and y such that topleft of mask1 == topleft of mask2


bird_img1 = pygame.transform.scale(bird_img, (120, 80))
bird_rect = bird_img1.get_rect()
bird_mask = pygame.mask.from_surface(bird_img1)
bird_mask_image = bird_mask.to_surface()

colour = (0, 255, 0)
obj = pygame.Surface((50, 50)).convert_alpha()
obj.fill(colour)
obj_rec = obj.get_rect()
obj_mask = pygame.mask.from_surface(obj)
obj_mask_img = obj_mask.to_surface()

speed = 1
clock = pygame.time.Clock()


while True:
    screen.fill('black')
    mpos = pygame.mouse.get_pos()
    bird_rect.top += speed
    bird_rect.left += speed
    screen.blit(bird_img1, bird_rect)

    # screen.blit(bird_mask_image, bird_rect.topleft)
    screen.blit(obj, (mpos[0] - 25, mpos[1] - 25))

    line = pygame.draw.line(screen, (255, 0, 0), (bird_rect.center), (mpos[0], mpos[1]), 4)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    if bird_mask.overlap(obj_mask, (mpos[0] -25 - bird_rect.x, mpos[1] -25 -bird_rect.y)):
        colour = (255, 0, 0)
    else:
        colour = (0, 255, 0)

    obj.fill(colour)
    pygame.display.update()
    clock.tick(60)
