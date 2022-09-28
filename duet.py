import pygame, math
from settings import *
import numpy as np
from duetParticle import DuetParticle

class Player:
    def __init__(self, surface, levelSpeed) -> None:
        self.screen = surface
        self.levelSpeed = levelSpeed

        self.ballRadius = HEIGHT/100

        self.ballY = HEIGHT/1.2

        self.ballDistance = 3.5
        self.rectBlue = pygame.Rect(WIDTH/self.ballDistance-self.ballRadius, self.ballY, self.ballRadius*2, self.ballRadius*2)
        self.rectRed = pygame.Rect(WIDTH-WIDTH/self.ballDistance-self.ballRadius, self.ballY, self.ballRadius*2, self.ballRadius*2)

        self.blueTrueCenter = self.rectBlue.center
        self.redTrueCenter = self.rectRed.center
        
        blue_redDist = self.rectRed.centerx-self.rectBlue.centerx
        self.rectDuet = pygame.Rect(self.rectBlue.centerx, self.rectBlue.centery-blue_redDist/2, blue_redDist, blue_redDist)

        self.angle = 0
        self.rotateSpeed_degrees = 4

        self.particleList = []

        self.pauseState = False

    def particleUpdate(self):
        for particle in self.particleList:
            particle.update(self.pauseState)
            if particle.faded():
                self.particleList.remove(particle)

    def particleHandler(self):
        self.particleList.append(DuetParticle(self.screen, self.rectBlue.center, self.rectBlue.width/2, self.levelSpeed, [0, 0, 255]))
        self.particleList.append(DuetParticle(self.screen, self.rectRed.center, self.rectRed.width/2, self.levelSpeed, [255, 0, 0]))
        self.particleUpdate()

    def rotate(self, point, degrees):
        radians = np.deg2rad(degrees)
        x,y = point
        offset_x, offset_y = self.rectDuet.center

        adjusted_x = (x - offset_x)
        adjusted_y = (y - offset_y)
        cos_rad = np.cos(radians)
        sin_rad = np.sin(radians)
        qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
        qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
        return qx, qy

    def controls(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.angle = self.rotateSpeed_degrees
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.angle = -self.rotateSpeed_degrees

        else:
            self.angle = 0
        
        if self.angle != 0 and not self.pauseState:
            self.blueTrueCenter = self.rotate(self.blueTrueCenter, self.angle)
            self.redTrueCenter = self.rotate(self.redTrueCenter, self.angle)

        self.rectBlue.center = self.blueTrueCenter
        self.rectRed.center = self.redTrueCenter

    def draw(self):
        pygame.draw.ellipse(self.screen, 'white', self.rectDuet, width=1)

        pygame.draw.ellipse(self.screen, 'blue', self.rectBlue)
        pygame.draw.ellipse(self.screen, 'red', self.rectRed)

    def update(self, pauseState):
        self.pauseState = pauseState
        self.controls()
        self.draw()
        self.particleHandler()