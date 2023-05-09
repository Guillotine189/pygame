import time

import pygame
pygame.font.init()
pygame.init()


SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player_image = pygame.image.load('./images/images.png')
p1 = pygame.image.load('./images/top.png')
p2 = pygame.image.load('./images/down.png')
menu_bg = pygame.image.load('./images/manu_1400x800.png')

upper_limit = SCREEN_HEIGHT - 154
lower_limit = -50

text = pygame.font.SysFont("monospace", 50)

class Button:
    def __init__(self,x,y,text):
        self.x = x
        self.y = y
        self.text = text
        self.draw()
    def draw(self):
        button_text = text.render(self.text, 1, 'black')
        button_rect = pygame.rect.Rect((self.x, self.y), (150, 50))
        if self.check_clicekd():
            pygame.draw.rect(screen, 'dark grey', button_rect, 0, 5)
        else:
            pygame.draw.rect(screen, 'light grey', button_rect, 0, 5)

        screen.blit(button_text, (self.x + 15, self.y + 2))


    def check_clicekd(self):
        m_pos = pygame.mouse.get_pos()
        left_cl = pygame.mouse.get_pressed()[0]
        button_rect = pygame.rect.Rect((self.x, self.y), (150, 50))
        if left_cl and button_rect.collidepoint(m_pos):
            return True
        else:
            return False

def player(z, x, y):

    screen.blit(z, (x, y))

def main_menu():
    pygame.display.set_caption("MENU")

    textbgd = text.render("MENU", 1, (255, 255, 255))

    while True:

        screen.fill("black")
        screen.blit(menu_bg, (0, 0))
        screen.blit(textbgd, (900,300))

        button1 = Button(800, 400, "PLAY")
        button2 = Button(1000, 400, "EXIT")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen2()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.check_clicekd():
                    screen2()
                if button2.check_clicekd():
                    pygame.quit()

        playerX = 0
        playerY = 200
        player(player_image,playerX, playerY)
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
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    playerY_ch -= up_speed


        playerY += playerY_ch
        playerX += playerX_ch
        playerY_ch += gravity

        if playerY >= upper_limit:
            playerY = upper_limit
            playerY_ch -= gravity

        if playerY < lower_limit:
            playerY = lower_limit
            playerY_ch += gravity


        player(player_image, playerX, playerY)
        pygame.display.update()

main_menu()
