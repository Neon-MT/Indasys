import pygame
from configLoader import *


class particle(pygame.sprite.Sprite):
    def __init__(self, startx, starty, radius, xvel, yvel, col):
        pygame.sprite.Sprite.__init__(self)
        self.x = startx
        self.y = starty
        self.radius = radius
        self.xvel = xvel
        self.yvel = yvel
        self.color = col

    def move(self):
        self.x += self.xvel
        self.y += self.yvel
        if self.x >= SCREEN_WIDTH+self.radius:
            self.kill()
        if self.y >= SCREEN_HEIGHT+self.radius:
            self.kill()

    def drawself(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class rain(pygame.sprite.Sprite):
    def __init__(self, startx, starty, width, yvel, xvel, col):
        pygame.sprite.Sprite.__init__(self)
        self.x = startx
        self.y = starty
        self.x2 = startx + xvel
        self.y2 = starty + yvel
        self.width = width
        self.xvel = xvel
        self.yvel = yvel
        self.color = col
        self.falltime = random.randint(5,60)

    def move(self):
        
        self.falltime -= 1
        if self.falltime <= 0:
            self.kill()
        self.x += self.xvel
        self.y += self.yvel
        self.x2 += self.xvel
        self.y2 += self.yvel
        # if self.x >= SCREEN_WIDTH:
        #     self.kill()
        # if self.y >= SCREEN_HEIGHT:
        #     self.kill()
    
    def drawself(self,screen):
        pygame.draw.line(screen, self.color, (self.x, self.y), (self.x2, self.y2), self.width)


class spark(pygame.sprite.Sprite):
    def __init__(self, startx, starty, radius, dirx, diry, col):
        self.x = startx
        self.y = starty
        self.dirx = dirx
        self.diry = diry
        self.radius = radius
        self.color = col
        if self.dirx > 0:
            self.xpoint = "RIGHT"
        else:
            self.xpoint = "LEFT"

        

    def move(self):
        if self.xpoint == "RIGHT":
            self.dirx -= 0.1
        else:
            self.dirx += 0.1

        if self.dirx == 0:
            self.kill()

        self.diry += 0.1

        self.x += self.dirx
        self.y += self.diry

    def drawself(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

#put sparks, lightning, dust, and rain here