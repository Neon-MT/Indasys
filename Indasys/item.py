import pygame
import os
from configLoader import *
def getImg(sheet, width, height, topleftx, toplefty, colorkey):
        
        surface = pygame.Surface((width, height))
        surface.blit(sheet, (0,0), (topleftx, toplefty, topleftx+width, toplefty + height))
        surface.set_colorkey(colorkey)
        return surface




class item(pygame.sprite.Sprite):
    def __init__(self, x, y, item, refined):
        pygame.sprite.Sprite.__init__(self)
        self.spawnx = x
        self.spawny = y
        self.fx = 0
        self.fy = 0
        self.px = 0
        self.py = 0
        self.prex, self.prey = 0,0
        self.tilemapx, self.tilemapy = x, y

        self.firstmove = True
        self.moving = False
        self.dir = 9

        self.x = x
        self.y = y
        self.sheet = pygame.image.load(os.path.dirname(__file__)+ "/assets/Materials.png")
        self.image = getImg(self.sheet, 16, 16, 16*(item-1), 16*refined, (0,0,0))
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()

    def update(self, x, y, toplayer, directions):
        self.toplayer = toplayer
        self.directions = directions
        if self.firstmove:
            self.look(self.toplayer, self.directions)
        if self.moving:
            if self.dir == 0:
                self.fy -=1
                self.prey -=1
            if self.dir == 1:
                self.fx +=1
                self.prex +=1
            if self.dir == 2:
                self.fy +=1
                self.prey +=1
            if self.dir == 3:
                self.fx -=1
                self.prex -=1

            if self.prex >= 16 :
                self.prex = 0
                #self.tilemapx += 1
            if self.prex <= 16 :
                self.prex = 0
                #self.tilemapx -= 1
            if self.prey >= 16 :
                self.prey = 0
                #self.tilemapy += 1
            if self.prey <= 16 :
                self.prey = 0
                #self.tilemapy -= 1

            self.x = x + self.fx + self.px + (self.spawnx * TILESIZE)
            self.y = y + self.fy + self.px + (self.spawny * TILESIZE)

            self.rect.x = self.x
            self.rect.y = self.y
        #print(self.dir)


    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def look(self, toplayer, directions):
        if toplayer[self.tilemapx+1, self.tilemapy] == 1:
            self.dir = directions[self.tilemapx+1, self.tilemapy]
            if self.firstmove:
                self.px = 16 * TILESIZE
                self.firstmove = False
            self.moving = True
        elif toplayer[self.tilemapx-1, self.tilemapy] == 1:
            self.dir = directions[self.tilemapx-1, self.tilemapy]
            if self.firstmove:
                self.px = -16 * TILESIZE
                self.firstmove = False
            self.moving = True
        elif toplayer[self.tilemapx, self.tilemapy+1] == 1:
            self.dir = directions[self.tilemapx, self.tilemapy+1]
            if self.firstmove:
                self.py = 16 * TILESIZE
                self.firstmove = False
            self.moving = True
        elif toplayer[self.tilemapx, self.tilemapy-1] == 1:
            self.dir = directions[self.tilemapx, self.tilemapy-1]
            if self.firstmove:
                self.py = -16 * TILESIZE
                self.firstmove = False
            self.moving = True
        else:
            self.dir = 9
            if self.firstmove:
                self.kill()
            else:
                self.moving = False
                self.firstmove = False

    def checkahead(self, toplayer):
        if self.dir == 0:
            if toplayer[self.tilemapx, self.tilemapy-1] != 1:
                self.moving = False
        elif self.dir == 1:
            if toplayer[self.tilemapx+1, self.tilemapy] != 1:
                self.moving = False
        elif self.dir == 2:
            if toplayer[self.tilemapx, self.tilemapy+1] != 1:
                self.moving = False
        elif self.dir == 3:
            if toplayer[self.tilemapx-1, self.tilemapy] != 1:
                self.moving = False
        else:
            self.moving = True


class copperItem(item):

    def __init__(self, x, y, refined):
        super().__init__(x, y, 0, refined)

class ironItem(item):
    def __init__(self, x, y, refined):
        super().__init__(x, y, 1, refined)

class stoneItem(item):
    def __init__(self, x, y, refined):
        super().__init__(x, y, 2, refined)

class coalItem(item):
    def __init__(self, x, y, refined):
        super().__init__(x, y, 3, refined)

class titaniumItem(item):
    def __init__(self, x, y, refined):
        super().__init__(x, y, 4, refined)

class leadItem(item):
    def __init__(self, x, y, refined):
        super().__init__(x, y, 5, refined)

class uraniumItem(item):
    def __init__(self, x, y, refined):
        super().__init__(x, y, 6, refined)

class thoriumItem(item):
    def __init__(self, x, y, refined):
        super().__init__(x, y, 7, refined)
