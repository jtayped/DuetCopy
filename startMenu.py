import pygame
from settings import *

class Menu:
    def __init__(self, surface, font, tinyFont) -> None:
        self.screen = surface
        self.font = font
        self.tinyFont = tinyFont

        self.username = ''

        self.spacer = 10

    def text(self):
        self.usernameInput = self.font.render('What is your username?', True, 'white')
        self.usernameInputWidth, self.usernameInputHeight = self.usernameInput.get_width(), self.usernameInput.get_height()

        self.usernameKeyboard = self.font.render(f'{self.username}', True, 'white')
        self.usernameKeyboardWidth, self.usernameKeyboardHeight = self.usernameKeyboard.get_width(), self.usernameKeyboard.get_height()

        self.next = self.font.render('Continue', True, 'green')
        self.nextRect = self.next.get_rect()
        self.nextRectWidth, self.nextRectHeight = self.next.get_width(), self.next.get_height()
        self.nextX, self.nextY = WIDTH/2-self.nextRectWidth/2, HEIGHT*0.65
        self.nextRect.x, self.nextRect.y = self.nextX, self.nextY

    def checkContinue(self):
        if self.nextRect.collidepoint(self.mousePress):
            return True
            
    def draw(self):
        usernameInputY = HEIGHT/2.5-self.usernameInputHeight/2
        self.usernameY = usernameInputY + self.usernameKeyboardHeight + self.spacer

        self.screen.blit(self.usernameInput, (WIDTH/2-self.usernameInputWidth/2, usernameInputY))
        self.screen.blit(self.usernameKeyboard, (WIDTH/2-self.usernameKeyboardWidth/2, self.usernameY))

        pygame.draw.rect(self.screen, 'green', self.nextRect, 2)
        self.screen.blit(self.next, (self.nextX, self.nextY))

    def update(self, username, mousePress):
        self.mousePress = mousePress
        self.username = username

        self.text()
        self.draw()

        if self.checkContinue():
            return True