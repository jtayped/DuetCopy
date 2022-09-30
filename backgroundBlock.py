import pygame, random

from settings import HEIGHT

class BackgroundBlock:
    def __init__(self, surface, pos, size, speed) -> None:
        self.screen = surface

        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.truePos = pygame.math.Vector2(self.rect.x, self.rect.y)

        self.color = random.randint(50, 150), random.randint(50, 150), random.randint(50, 150)

        self.width = 2
        self.speed = speed
    
    def offScreen(self):
        return self.rect.top > HEIGHT

    def movement(self):
        self.truePos.y += self.speed
        self.rect.y = int(self.truePos.y)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, width=self.width)
    
    def update(self, pauseState):
        if not pauseState:
            self.movement()
        self.draw()
