import pygame
from settings import *
from level import Level
from startMenu import Menu

pygame.init()
#pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duet")
clock = pygame.time.Clock()
menuFont = pygame.font.SysFont('AGENCYB.TTF', 40)
font = pygame.font.SysFont('AGENCYB.TTF', 75)
tinyFont = pygame.font.SysFont('AGENCYB.TTF', 25)

menu = Menu(screen, menuFont, tinyFont)

username = ''
running = True
pos = (0, 0)

while running:
    clock.tick(FPS)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha() and len(username) < 10:
                username += event.unicode

            elif event.key == pygame.K_BACKSPACE and len(username) > 0:
                username = username.rstrip(username[-1])
            
            elif event.key == pygame.K_RETURN and len(username) > 2:
                running = False

    screen.fill('black')
    if menu.update(username, pos):
        running = False
    
    pygame.display.flip() 


level = Level(screen, font, tinyFont, username)         

#pygame.mixer.music.load('media/elevatormusic.mp3')

#pygame.mixer.music.play()

running = True
while running:

    clock.tick(FPS)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

    screen.fill('black')
    level.update(clock.get_fps())
    
    pygame.display.flip()       

pygame.quit()