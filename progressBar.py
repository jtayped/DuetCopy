import pygame
from settings import *

class ProgressBar:
    def __init__(self, surface, score, maxScore) -> None:
        self.screen = surface

        self.maxScore = maxScore
        self.score = score

        self.percentage = 0

        self.height = HEIGHT/100

        self.rect = pygame.Rect(0, HEIGHT-self.height, 0, self.height)

    def calculateProgressBar(self):
        self.percentage = self.score/self.maxScore*100

        self.rect.width = WIDTH/100*self.percentage

    def draw(self):
        pygame.draw.rect(self.screen, 'green', self.rect)
    
    def update(self, score):
        self.score = score
        self.calculateProgressBar()
        self.draw()