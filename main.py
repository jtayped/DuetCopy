import pygame
from settings import *
from level import Level

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duet")
clock = pygame.time.Clock()
font = pygame.font.SysFont('AGENCYB.TTF', 75)
tinyFont = pygame.font.SysFont('AGENCYB.TTF', 25)

username = 'jtayped'
level = Level(screen, font, tinyFont, username)         

pygame.mixer.music.load('media/elevatormusic.mp3')

pygame.mixer.music.play()

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