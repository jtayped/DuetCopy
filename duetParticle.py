import pygame, random
from settings import *

class DuetParticle:
    def __init__(self, surface, pos, radius, speed, color) -> None:
        self.screen = surface

        self.color = color
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.radius = radius

        self.speed = pygame.math.Vector2(0, speed)

        self.radiusDegradeSpeed = 0.225

        if self.color[0] == 255:
            self.colorBall = 'red'

        else:
            self.colorBall = 'blue'

    def movement(self):
        
        self.pos.y += self.speed.y
        self.pos.x += round(random.uniform(-0.1, 0.1), 2)
    
    def fade(self):
        self.radius -= self.radiusDegradeSpeed
    
    def faded(self):
        return self.radius <= 0
     
    def draw(self):
        pygame.draw.circle(self.screen, self.colorBall, self.pos, self.radius)
    
    def update(self, pauseState):
        if not pauseState:
            self.movement()
            self.fade()
        self.draw()