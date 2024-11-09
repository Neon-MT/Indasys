import pygame
import os
from configLoader import *
from player import *
from item import *

pygame.init()

fixscreen = pygame.display.set_mode((0,0))

def loadSpriteSheets():
        return pygame.image.load(os.path.dirname(__file__)+ "/assets/oreSpriteSheet.png").convert(), pygame.image.load(os.path.dirname(__file__)+ "/assets/drillSpriteSheet.png").convert(), pygame.image.load(os.path.dirname(__file__)+ "/assets/ConveyorSpriteSheet.png").convert(),pygame.image.load(os.path.dirname(__file__)+ "/assets/ConveyorTurns.png")

def loadMoreSheets():
    return pygame.image.load(os.path.dirname(__file__)+ "/assets/Teleporter.png")
groundsheet,drillsheet,conveyorsheet,TurnConveyorsheet = loadSpriteSheets()
Teleportersheet = loadMoreSheets()


def getImg(sheet, width, height, topleftx, toplefty, colorkey):
        
        surface = pygame.Surface((width, height))
        surface.blit(sheet, (0,0), (topleftx, toplefty, topleftx+width, toplefty + height))
        surface.set_colorkey(colorkey)
        return surface









class tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img



        self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))

        self.tilex = x * TILESIZE
        self.tiley = y * TILESIZE
        
        self.width = TILESIZE
        self.height = TILESIZE

        self.rect = self.image.get_rect()

        self.tilemapx = x
        self.tilemapy = y

        self.game = game
        self.drawSelect = False
        self.playerdir = 0
        self.clickx = 0
        self.clicky = 0




    def update(self, x, y, mousedown, game):
        self.tilex = x + self.tilemapx * TILESIZE
        self.tiley = y + self.tilemapy * TILESIZE

        self.rect.x = self.tilex
        self.rect.y = self.tiley

        if mousedown:
            mx, my = pygame.mouse.get_pos()
            if self.rect.collidepoint(mx,my):
                self.clickx = self.tilex/TILESIZE
                self.clicky = self.tiley/TILESIZE
                game.clickedTile(self.tilemapx, self.tilemapy)


    def draw(self, screen):
        screen.blit(self.tilex, self.tiley)
            

        if self.drawSelect:
            pygame.draw.rect(screen,(255,0,0), self.image.get_rect(), 3)




class toptile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
        self.madeitems = pygame.sprite.Group()


        self.tilex = x * TILESIZE
        self.tiley = y * TILESIZE

        
        self.width = TILESIZE
        self.height = TILESIZE

        self.rect = self.image.get_rect()

        self.tilemapx = x
        self.tilemapy = y

        self.game = game
        self.drawSelect = False
        self.playerdir = 0


    def update(self, x, y, mousedelete, game):
        self.tilex = x + self.tilemapx * TILESIZE
        self.tiley = y + self.tilemapy * TILESIZE

        self.rect.x = self.tilex
        self.rect.y = self.tiley


        if mousedelete:
            mx, my = pygame.mouse.get_pos()
            if self.rect.collidepoint(mx,my):
                game.deleteTile(self.tilemapx, self.tilemapy)
                self.kill()

    def draw(self, screen):
        screen.blit(self.tilex, self.tiley)
            

        if self.drawSelect:
            pygame.draw.rect(screen,(255,0,0), self.image.get_rect(), 3)


class drillobj(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img, extracting, item, lvl):
        pygame.sprite.Sprite.__init__(self)
        self.image = img

        self.extracting = extracting
        self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
        self.madeitems = pygame.sprite.Group()

        self.lvl = lvl

        self.tilex = x * TILESIZE
        self.tiley = y * TILESIZE
        self.drilltick = 0

        self.drill = item

        
        self.width = TILESIZE
        self.height = TILESIZE

        self.rect = self.image.get_rect()

        self.tilemapx = x
        self.tilemapy = y

        self.game = game
        self.drawSelect = False
        self.playerdir = 0


    def update(self, x, y, mousedelete, game):
        self.tilex = x + self.tilemapx * TILESIZE
        self.tiley = y + self.tilemapy * TILESIZE

        self.rect.x = self.tilex
        self.rect.y = self.tiley
        if self.drill:
            self.drilltick += 1
            if self.drilltick >= 400-(self.lvl*50):
                self.drilltick = 0
                self.spawnitem()

        if mousedelete:
            mx, my = pygame.mouse.get_pos()
            if self.rect.collidepoint(mx,my):
                game.deleteTile(self.tilemapx, self.tilemapy)
                self.kill()


    def draw(self, screen):
        screen.blit(self.tilex, self.tiley)
            

        if self.drawSelect:
            pygame.draw.rect(screen,(255,0,0), self.image.get_rect(), 3)

    def spawnitem(self):
        self.game.createItem(self.tilemapx, self.tilemapy, self.extracting)



class conveyor(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img, direction, turn):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
        self.tilex = x * TILESIZE
        self.tiley = y * TILESIZE
        self.turn = turn

        #figure this out \/
        #self.imageframes = []
        
        self.width = TILESIZE
        self.height = TILESIZE

        self.rect = self.image.get_rect()

        self.direction = direction

        self.tilemapx = x
        self.tilemapy = y

        self.game = game
        self.drawSelect = False
        self.playerdir = 0


    def update(self, x, y, frame, mousedelete, game):
        self.tilex = x + self.tilemapx * TILESIZE
        self.tiley = y + self.tilemapy * TILESIZE

        self.rect.x = self.tilex
        self.rect.y = self.tiley
        if self.turn != 9:
            self.image = getImg(TurnConveyorsheet, 16,16, 16*(frame - 1),16*self.turn, (0,0,0)).convert()
        else:
            self.image = getImg(conveyorsheet, 16,16, 16*(frame - 1),16*self.direction, (0,0,0)).convert()
        #self.image = getImg(conveyorsheet, 16,16, 16*(frame - 1),16*self.direction,(0,0,0)).convert()
        self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))

        if mousedelete:
            mx, my = pygame.mouse.get_pos()
            if self.rect.collidepoint(mx,my):
                game.deleteTile(self.tilemapx, self.tilemapy)
                self.kill()


    def checkProx(self, toplayer, directions, turns):
        up = self.tilemapy-1
        down = self.tilemapy+1
        left = self.tilemapx-1
        right = self.tilemapx+1

        #check turns:
        try:
            if toplayer[self.tilemapx, down] == 1 and self.direction == 3 and turns[self.tilemapx, down] == 9 and directions[self.tilemapx, down] == 0:
                self.turn = 1
            elif toplayer[self.tilemapx, down] == 1 and self.direction == 1 and turns[self.tilemapx, down] == 9 and directions[self.tilemapx, down] == 0:
                self.turn = 0
            elif toplayer[self.tilemapx, up] == 1 and self.direction == 1 and turns[self.tilemapx, up] == 9 and directions[self.tilemapx, up] == 2:
                self.turn = 2
            elif toplayer[self.tilemapx, up] == 1 and self.direction == 3 and turns[self.tilemapx, up] == 9 and directions[self.tilemapx, up] == 2:
                self.turn = 3
            elif toplayer[right, self.tilemapy] == 1 and self.direction == 0 and turns[right, self.tilemapy] == 9 and directions[right, self.tilemapy] == 3:
                self.turn = 4
            elif toplayer[right, self.tilemapy] == 1 and self.direction == 2 and turns[right, self.tilemapy] == 9 and directions[right, self.tilemapy] == 3:
                self.turn = 5
            elif toplayer[left, self.tilemapy] == 1 and self.direction == 0 and turns[left, self.tilemapy] == 9 and directions[left, self.tilemapy] == 1:
                self.turn = 6
            elif toplayer[left, self.tilemapy] == 1 and self.direction == 2 and turns[left, self.tilemapy] == 9 and directions[left, self.tilemapy] == 1:
                self.turn = 7
            else:
                self.turn = 9
        except:
            self.turn = 9



        return self.turn, self.tilemapx, self.tilemapy

    def draw(self, screen):
        if self.drawSelect:
            pygame.draw.rect(screen,(255,0,0), self.image.get_rect(), 3)
        
        screen.blit(self.tilex, self.tiley)


class Core(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.tilemapx = x
        self.tilemapy = y

        self.width = 32
        self.height = 32
        self.image = pygame.image.load(os.path.dirname(__file__)+ "/assets/Core.png").convert()
        self.image = pygame.transform.scale(self.image, (TILESIZE * 2,TILESIZE * 2))
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.tilex = x + self.tilemapx * TILESIZE
        self.tiley = y + self.tilemapy * TILESIZE

        self.rect.x = self.tilex
        self.rect.y = self.tiley

    def draw(self, screen):
        screen.blit(self.image, (self.tilex, self.tiley))


class teletile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
        self.madeitems = pygame.sprite.Group()


        self.tilex = x * TILESIZE
        self.tiley = y * TILESIZE

        
        self.width = TILESIZE
        self.height = TILESIZE

        self.rect = self.image.get_rect()

        self.tilemapx = x
        self.tilemapy = y

        self.game = game
        self.drawSelect = False
        self.playerdir = 0


    def update(self, x, y, mousedelete, game):
        self.tilex = x + self.tilemapx * TILESIZE
        self.tiley = y + self.tilemapy * TILESIZE

        self.rect.x = self.tilex
        self.rect.y = self.tiley


        if mousedelete:
            mx, my = pygame.mouse.get_pos()
            if self.rect.collidepoint(mx,my):
                game.deleteTile(self.tilemapx, self.tilemapy)
                self.kill()

    def draw(self, screen):
        screen.blit(self.tilex, self.tiley)
            

        if self.drawSelect:
            pygame.draw.rect(screen,(255,0,0), self.image.get_rect(), 3)

class storagetile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
        self.madeitems = pygame.sprite.Group()


        self.tilex = x * TILESIZE
        self.tiley = y * TILESIZE

        
        self.width = TILESIZE
        self.height = TILESIZE

        self.rect = self.image.get_rect()

        self.tilemapx = x
        self.tilemapy = y

        self.game = game
        self.drawSelect = False
        self.playerdir = 0


    def update(self, x, y, mousedelete, game):
        self.tilex = x + self.tilemapx * TILESIZE
        self.tiley = y + self.tilemapy * TILESIZE

        self.rect.x = self.tilex
        self.rect.y = self.tiley


        if mousedelete:
            mx, my = pygame.mouse.get_pos()
            if self.rect.collidepoint(mx,my):
                game.deleteTile(self.tilemapx, self.tilemapy)
                self.kill()

    def draw(self, screen):
        screen.blit(self.tilex, self.tiley)
            

        if self.drawSelect:
            pygame.draw.rect(screen,(255,0,0), self.image.get_rect(), 3)

class nodetile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image = pygame.transform.scale(self.image, (TILESIZE,TILESIZE))
        self.madeitems = pygame.sprite.Group()


        self.tilex = x * TILESIZE
        self.tiley = y * TILESIZE

        
        self.width = TILESIZE
        self.height = TILESIZE

        self.rect = self.image.get_rect()

        self.tilemapx = x
        self.tilemapy = y

        self.game = game
        self.drawSelect = False
        self.playerdir = 0


    def update(self, x, y, mousedelete, game):
        self.tilex = x + self.tilemapx * TILESIZE
        self.tiley = y + self.tilemapy * TILESIZE

        self.rect.x = self.tilex
        self.rect.y = self.tiley


        if mousedelete:
            mx, my = pygame.mouse.get_pos()
            if self.rect.collidepoint(mx,my):
                game.deleteTile(self.tilemapx, self.tilemapy)
                self.kill()

    def draw(self, screen):
        screen.blit(self.tilex, self.tiley)
            

        if self.drawSelect:
            pygame.draw.rect(screen,(255,0,0), self.image.get_rect(), 3)


class Ground(tile):
    def __init__(self, game, x, y, biomeid):
        self.groundtilesheetx = biomeid * 4
        variation = random.randint(0,2)
        self.image = getImg(groundsheet, 16,16,16*(self.groundtilesheetx + variation),0,(0,0,0))
        super().__init__(game, x, y, self.image)

class CopperOre(tile):
    def __init__(self, game, x, y, biomeid):
        self.groundtilesheetx = biomeid * 4
        variation = random.randint(0,2)
        self.image = getImg(groundsheet, 16,16,16*(self.groundtilesheetx + variation),16,(0,0,0))
        super().__init__(game, x, y, self.image)

class IronOre(tile):
    def __init__(self, game, x, y, biomeid):
        self.groundtilesheetx = biomeid * 4
        variation = random.randint(0,2)
        self.image = getImg(groundsheet, 16,16,16*(self.groundtilesheetx + variation),32,(0,0,0))
        super().__init__(game, x, y, self.image)

class Stone(tile):
    def __init__(self, game, x, y, biomeid):
        self.groundtilesheetx = biomeid * 4
        variation = random.randint(0,2)
        self.image = getImg(groundsheet, 16,16,16*(self.groundtilesheetx + variation),48,(0,0,0))
        super().__init__(game, x, y, self.image)

class CoalOre(tile):
    def __init__(self, game, x, y, biomeid):
        self.groundtilesheetx = biomeid * 4
        variation = random.randint(0,2)
        self.image = getImg(groundsheet, 16,16,16*(self.groundtilesheetx + variation),64,(0,0,0))
        super().__init__(game, x, y, self.image)
    
class TitaniumOre(tile):
    def __init__(self, game, x, y, biomeid):
        self.groundtilesheetx = biomeid * 4
        variation = random.randint(0,2)
        self.image = getImg(groundsheet, 16,16,16*(self.groundtilesheetx + variation),80,(0,0,0))
        super().__init__(game, x, y, self.image)

class LeadOre(tile):
    def __init__(self, game, x, y, biomeid):
        self.groundtilesheetx = biomeid * 4
        variation = random.randint(0,2)
        self.image = getImg(groundsheet, 16,16,16*(self.groundtilesheetx + variation),96,(0,0,0))
        super().__init__(game, x, y, self.image)

class UraniumOre(tile):
    def __init__(self, game, x, y, biomeid):
        self.groundtilesheetx = biomeid * 4
        variation = random.randint(0,2)
        self.image = getImg(groundsheet, 16,16,16*(self.groundtilesheetx + variation),112,(0,0,0))
        super().__init__(game, x, y, self.image)

class ThoriumOre(tile):
    def __init__(self, game, x, y, biomeid):
        self.groundtilesheetx = biomeid * 4
        variation = random.randint(0,2)
        self.image = getImg(groundsheet, 16,16,16*(self.groundtilesheetx + variation),128,(0,0,0))
        super().__init__(game, x, y, self.image)

class Drill(drillobj):
    def __init__(self, game, x, y, lvl, above):

        self.image = getImg(drillsheet, 16,16,16*above,16*lvl,(0,0,0))

        super().__init__(game, x, y, self.image, above, True, lvl)
        
class Conveyor(conveyor):
    def __init__(self, game, x, y, direction):
        self.image = getImg(conveyorsheet, 16,16, 0,16*direction, (0,0,0))
        super().__init__(game, x, y, self.image, direction, 0)

class Powernode(nodetile):
    def __init__(self,game, x, y):
        self.image = pygame.image.load(os.path.dirname(__file__)+ "/assets/powerNode.png").convert()
        super().__init__(game, x, y , self.image)

class Teleporter(teletile):
    def __init__(self, game, x, y, direction):
        self.image = getImg(Teleportersheet, 16,16, 0,16*direction, (0,0,0))
        super().__init__(game, x, y, self.image)

class Battery(storagetile):
    def __init__(self,game, x, y):
        self.image = pygame.image.load(os.path.dirname(__file__)+ "/assets/battery.png").convert()
        super().__init__(game, x, y , self.image)