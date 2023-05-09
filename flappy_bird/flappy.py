import pygame
pygame.font.init()
pygame.init()


SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player_image = pygame.image.load('./images/images.png')
menu_bg = pygame.image.load('./images/manu_1400x800.png')

upper_limit = SCREEN_HEIGHT - 154
lower_limit = -50

text = pygame.font.SysFont("monospace", 50)

def player(x,y):

    screen.blit(player_image, (x, y))

def main_menu():
    pygame.display.set_caption("MENU")

    textbgd = text.render("MENU", 1, (255, 255, 255))
    while True:

        screen.fill("black")
        screen.blit(menu_bg, (0, 0))
        screen.blit(textbgd, (900,100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen2()

        playerX = 0
        playerY = 200
        player(playerX, playerY)
        pygame.display.update()


def screen2():
    up_speed = 7
    gravity = 0.1
    pygame.display.set_caption("FLAPPY BIRD")
    background = pygame.image.load("./images/flappy_1400x800.png")

    playerX = 0
    playerY = 200
    playerX_ch = 0
    playerY_ch = 0

    while True:

        screen.fill("black")
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playerY_ch -= up_speed
                if event.key == pygame.K_BACKSPACE:
                    main_menu()

        playerY += playerY_ch
        playerX += playerX_ch
        playerY_ch += gravity

        if playerY >= upper_limit:
            playerY = upper_limit
            playerY_ch -= gravity

        if playerY < lower_limit:
            playerY = lower_limit
            playerY_ch += gravity


        player(playerX, playerY)
        pygame.display.update()

main_menu()
