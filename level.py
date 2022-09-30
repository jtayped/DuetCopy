import random, math, csv, datetime, pygame
from settings import *
from duet import Player
from obstacle import Obstacle
from backgroundBlock import BackgroundBlock
from progressBar import ProgressBar
import pandas as pd

class Level:
    def __init__(self, surface, scoreFont, tinyFont, username) -> None:
        self.screen = surface
        self.font = scoreFont
        self.tinyFont = tinyFont
        self.username = username

        self.obstacleSpeed = 4
        self.player = Player(self.screen, self.obstacleSpeed)
        self.blueRedDist = self.player.rectRed.left - self.player.rectBlue.right

        self.obstacleList = []
        self.obstacleBuffer = 10
        self.borderSpacer = 30
        self.spacer = 180/self.player.rotateSpeed_degrees*self.obstacleSpeed
        self.obstaclesInScreen = math.ceil(HEIGHT/self.spacer)

        self.backgroundBlockList = []
        self.nBlocks = 15
        for i in range(self.nBlocks):
            self.generateBackgroundBlock(onScreen=True)

        self.score = 0
        
        df = pd.read_csv('scores.csv')
        scoresColumn = df[df.columns[2]]
        self.maxAllTimeScore = max(scoresColumn)
        #self.maxAllTimeScore = 20

        index = df.index
        condition = df['score'] == self.maxAllTimeScore
        scoreIndex = index[condition]

        scoreRow = scoreIndex.tolist()

        self.maxDate = df['date'][scoreRow].values[0]
        self.maxDate = self.maxDate.split(" ")[0]

        self.maxUsername = df['username'][scoreRow].values[0]

        self.progresBar = ProgressBar(self.screen, self.score, self.maxAllTimeScore)

        self.levelUp = False
        self.obstacleSpeedMultiplier = 1.25
        self.levelFreq = 0
        self.levelStep = 50
        self.scoreSpeed = 0.05
        self.wave = 1

        self.pause = False

    def pauseControl(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            self.pause = True
        elif key[pygame.K_BACKSPACE]:
            self.pause = False

    def appendScoreCSV(self):
        info=[datetime.datetime.now(), self.username, int(self.score), self.wave]
        with open('scores.csv', 'a', newline='') as file:
            Fileout=csv.writer(file, delimiter=',',quoting=csv.QUOTE_NONNUMERIC)
            Fileout.writerow(info)
            file.close()

    def generateBackgroundBlock(self, onScreen=False):
        width = height = random.randint(30, 200)
        speed = random.random()*self.obstacleSpeed/2.5

        if onScreen:
            pos = (random.randint(0, WIDTH-width), random.randint(-HEIGHT/2, HEIGHT-height))
        else:
            pos = (random.randint(0, WIDTH-width), random.randint(-HEIGHT, -height))

        self.backgroundBlockList.append(BackgroundBlock(self.screen, pos, (width, height), speed))   

    def backgroundHandler(self):
        if len(self.backgroundBlockList) < self.nBlocks:
            self.generateBackgroundBlock()
        
        for block in self.backgroundBlockList:
            block.update(self.pause)
            if block.offScreen():
                self.backgroundBlockList.remove(block)

    def reset(self):
        if self.score >= 15:
            self.appendScoreCSV()
        self.__init__(self.screen, self.font, self.tinyFont, self.username)

    def obstacleUpdate(self):
        for obstacle in self.obstacleList:
            if obstacle.offScreen():
                self.obstacleList.remove(obstacle)
                continue

            elif self.player.rectBlue.colliderect(obstacle.rect) or self.player.rectRed.colliderect(obstacle.rect):
                self.reset()

            obstacle.update(self.obstacleSpeed, self.pause)

    def obstacleHandler(self):
        self.levelFreq += self.scoreSpeed
        self.obstacleUpdate()

        if self.levelFreq >= self.levelStep:
            self.levelUp = True

            if len(self.obstacleList) == 0:
                self.obstacleSpeed = int(self.obstacleSpeed*1.4)
                self.player.rotateSpeed_degrees = int(self.player.rotateSpeed_degrees*1.3)

                self.spacer = 180/self.player.rotateSpeed_degrees * self.obstacleSpeed

                self.levelFreq = 0
                self.wave += 1

                self.obstaclesInScreen = math.ceil(HEIGHT/self.spacer)

                self.levelUp = False

        if len(self.obstacleList) < self.obstaclesInScreen and not self.levelUp:

            width, height = WIDTH/1.8-self.borderSpacer, HEIGHT/150
            length = 1

            randomInt = random.randint(1, 3)
            randomInt2 = random.randint(1, 2)

            if len(self.obstacleList) == 0:
                lastObstacleY = -height
            
            else:
                lastObstacleY = self.obstacleList[-1].rect.y

            if randomInt == 1 and randomInt2 == 1:
                lastObstacleY -= self.spacer

            randomInt = random.randint(1, 4)

            if randomInt == 1:
                for i in range(length):
                    self.obstacleList.append(Obstacle(self.screen, (width, height), (self.borderSpacer, lastObstacleY-(i*self.spacer+self.spacer)), self.obstacleSpeed))  

            elif randomInt == 2:
                for i in range(length):
                    self.obstacleList.append(Obstacle(self.screen, (width, height), (WIDTH-width-self.borderSpacer, lastObstacleY-(i*self.spacer+self.spacer)), self.obstacleSpeed))  

            elif randomInt == 3 and randomInt2 == 2:
                self.obstacleList.append(Obstacle(self.screen, (width/2, height), (WIDTH/2-width/2/2, lastObstacleY-self.spacer), self.obstacleSpeed))

            elif randomInt == 4 and randomInt2 == 1:
                self.obstacleList.append(Obstacle(self.screen, (width/2, height), (WIDTH/2-width/4 - width/3, lastObstacleY-self.spacer), self.obstacleSpeed))
                lastObstacleY -= self.spacer
                self.obstacleList.append(Obstacle(self.screen, (width/2, height), (WIDTH/2-width/4 + width/3, lastObstacleY-self.spacer), self.obstacleSpeed))


    def scoreBoard(self):
        spacer = 5
        scoreText = self.font.render(f'{int(self.score)}', True, 'white')
        scoreWidth, scoreHeight = scoreText.get_width(), scoreText.get_height()

        waveText = self.tinyFont.render(f'Wave: {self.wave}', True, 'white')
        waveWidth = waveText.get_width()

        maxScoreText = self.font.render(f'{self.maxAllTimeScore}', True, 'white')
        maxScoreHeight = maxScoreText.get_height()

        maxDateText = self.tinyFont.render(f'{self.maxDate}', True, 'white')
        maxDateHeight = maxDateText.get_height()

        maxUsernameText = self.tinyFont.render(f'{self.maxUsername}', True, 'white')

        loggedInText = self.tinyFont.render(f'Logged in as:', True, 'white')
        loggedInWidth, loggedInHeight = loggedInText.get_width(), loggedInText.get_height()

        usernameText = self.tinyFont.render(f'{self.username}', True, 'white')
        usernameWidth = usernameText.get_width()

        #fpsText = self.tinyFont.render(f'FPS: {self.fps}', True, 'white')
        #fpsHeight = fpsText.get_height()

        self.screen.blit(scoreText, (WIDTH/2-scoreWidth/2, spacer))
        self.screen.blit(waveText, (WIDTH/2-waveWidth/2, scoreHeight+spacer*2))

        self.screen.blit(maxScoreText, (spacer, spacer))
        self.screen.blit(maxDateText, (spacer, maxScoreHeight+spacer*2))
        self.screen.blit(maxUsernameText, (spacer, maxScoreHeight+maxDateHeight+spacer*3))
        
        self.screen.blit(loggedInText, (WIDTH-loggedInWidth-spacer, spacer))
        self.screen.blit(usernameText, (WIDTH-usernameWidth-spacer, loggedInHeight+spacer*2))

        #self.screen.blit(fpsText, (0, HEIGHT-fpsHeight))
        
    def update(self, fps):
        if not self.pause:
            self.score += self.scoreSpeed
        self.fps = int(fps)
        self.pauseControl()
        self.backgroundHandler()
        self.player.update(self.pause)
        self.obstacleHandler()
        self.scoreBoard()
        self.progresBar.update(self.score)