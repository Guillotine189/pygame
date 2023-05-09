import pygame

pygame.init()  # initialize pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Test window")
icon_right = pygame.image.load('./all_image/goku/baseright.png')
icon_left = pygame.image.load("./all_image/goku/baseleft.png")
icon_a = pygame.image.load('./all_image/goku/about.png')
icon_b = pygame.image.load('./all_image/goku/evolving.png')
icon_c = pygame.image.load('./all_image/goku/evolved.png')
curr_image = icon_right
background = pygame.image.load("./all_image/back.png")

pygame.display.set_icon(icon_right)

playerx = 0
playery = SCREEN_HEIGHT
playerx_change = 0
playery_change = 0

form = 'B'
f = 'B'

speed = 19
gravity = 17.8



def change_up(a,b,c,f):
	pygame.time.wait(500)
	curr_image = a
	player(curr_image, playerx, playery)
	pygame.display.update()
	pygame.time.wait(500)
	curr_image = b
	player(curr_image, playerx, playery)
	pygame.display.update()
	pygame.time.wait(500)
	curr_image = c
	player(curr_image, playerx, playery)
	pygame.display.update()
	form = f

def change_down(a,b,f):
	pygame.time.wait(1000)
	curr_image = a
	player(curr_image, playerx, playery)
	pygame.display.update()
	pygame.time.wait(1000)
	curr_image = b
	player(curr_image, playerx, playery)
	pygame.display.update()
	form = f

def player(ic,x,y):
	screen.blit(ic, (x, y))


running = True
while running:
	screen.fill((0, 0, 0))
	screen.blit(background, (0, 0))


	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				print("UP PRESSED")
				playery_change = -speed
			if event.key == pygame.K_DOWN:
				print("DOWN PRESSED")
				playery_change = speed
				pygame.display.update()
			if event.key == pygame.K_LEFT:
				print("LEFT PRESSED")
				player(icon_left,playerx, playery)
				curr_image = icon_left
				playerx_change = -speed
			if event.key == pygame.K_RIGHT:
				player(icon_right,playerx, playery)
				print("RIGHT PRESSED")
				curr_image = icon_right
				playerx_change = speed


			if event.key == pygame.K_SPACE:
				if form == 'B':
					print("SPACE PRESSED")
					change_up(icon_a, icon_b, icon_c, 'SSJB')
					playery_change = gravity





		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				print("UP RELEASED")
				playery_change = gravity
			if event.key == pygame.K_DOWN:
				print("DOWN RELEASED")
				playery_change = 0
				playery_change = gravity
			if event.key == pygame.K_LEFT:
				print("LEFT RELEASED")
				playerx_change = 0
				playery_change = gravity
			if event.key == pygame.K_RIGHT:
				print("RIGHT RELEASED")
				playerx_change = 0
				playery_change = gravity
			if event.key == pygame.K_SPACE:
				print("SPACE RELEASED")


	playerx += playerx_change
	playery += playery_change
	if playerx < 0:
		playerx = 0
	elif playerx > SCREEN_WIDTH - 150:
		playerx = SCREEN_WIDTH - 150

	if playery < 0:
		playery = 0
	elif playery > SCREEN_HEIGHT - 180:
		playery = SCREEN_HEIGHT - 180

	player(curr_image,playerx,playery)
	pygame.display.update()
