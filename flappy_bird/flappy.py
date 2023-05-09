import pygame

pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("FLAPPY BIRD")
background = pygame.image.load("./images/flappy_1400x800.png")
player_image = pygame.image.load('./images/images.png')

playerX = 0
playerY = 200
playerX_ch = 0
playerY_ch = 0
up_speed = 7
gravity = 0.1

def player(x,y):
    screen.blit(player_image, (x, y))


running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playerY_ch -= up_speed





    playerY += playerY_ch
    playerX += playerX_ch
    playerY_ch += gravity

    if playerY >= SCREEN_HEIGHT - 154:
        playerY = SCREEN_HEIGHT - 154
        playerY_ch -= gravity

    if playerY < 0:
        playerY = 0
        playerY_ch += gravity


    player(playerX, playerY)
    pygame.display.update()
