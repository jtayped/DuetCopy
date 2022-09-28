import pygame
from settings import *

class Obstacle:
    def __init__(self, surface, size, pos, speed, rotating=False) -> None:
        self.screen = surface
        
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

        self.speed = speed

    def offScreen(self):
        return self.rect.top > HEIGHT

    def draw(self):
        pygame.draw.rect(self.screen, 'white', self.rect)

    def movement(self):
        self.rect.y += self.speed
        
    def update(self, speed, pauseState):
        self.speed = speed
        if not pauseState:
            self.movement()
        self.draw()