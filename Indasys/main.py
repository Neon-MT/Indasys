import pygame
import sys
import os
from player import *
from tile import *
from configLoader import *
from Map import *
from sounds import *
import pygame.font
from ui import *
from weather import *
from pygame.locals import *
from particle import *

pygame.font.init()
pygame.init()

flags = DOUBLEBUF | pygame.RESIZABLE
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT] , flags, 16)


pygame.mouse.set_visible(False)

pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

pygame.display.set_caption("Game")
afont = pygame.font.SysFont('Ariel', 50)
screen.blit(afont.render("Loading...", False, (255,255,255)), (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
pygame.display.flip()


pointer = pygame.image.load(os.path.dirname(__file__)+ "/assets/pointer.png")
pointer = pygame.transform.scale(pointer, (50,50))

class main():
    def __init__(self):
        self.Player = Player(self)
        self.running = True

        self.visableScreen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.weatherScreen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()
        self.tilegroup = pygame.sprite.Group()
        self.topgroup = pygame.sprite.Group()
        self.conveyorgroup = pygame.sprite.Group()
        self.itemgroup = pygame.sprite.Group()

        self.font = pygame.font.SysFont('Ariel', 50)
        self.tileMap = np.array ([[0 for x in range(MAPSIZE)] for y in range(MAPSIZE)])
        self.Speaker = Speaker(False)
        self.pastTitle = False
        self.title = titleScreen()
        self.corex = random.randint(0,MAPSIZE-1)
        self.corey = random.randint(0,MAPSIZE-1)
        self.frame = 0
        self.passedframes = 0
        self.drilltick = 0
        self.err = False
        self.biomeid = 2
        self.md = False
        self.mdel = False
        self.selection = 1
        self.clickx = None
        self.clicky = None
        self.weatherbrightness = 0
        self.relx = 0
        self.tileclickdir = 0
        self.rely = 0
        self.drillprogression = 0
        self.drillselection = 0
        self.uier = ui(self.visableScreen)
        self.stormHandler = stormHandler()
        self.clouds = self.stormHandler.thunderStorm(10, 3000)
        self.Speaker.rainsound()
        self.mainloop()

        
    def mainloop(self):
        if not self.pastTitle:
            Speaker(True)
            while not self.pastTitle:
                #if savefile doesn't exist:
                if self.err:
                    updates = self.title.update(screen, True)
                    self.err = False
                #otherwise:
                else:
                    updates = self.title.update(screen, False)
                #if clicked on "load game":
                if updates == 1:
                    self.gameData = askLoad(1)
                    if self.gameData == False:
                        self.err = True
                    #loads game from save
                    else:
                        self.tileMap = self.gameData["tilemap"]
                        self.toplayer = self.gameData["toplayer"]
                        self.directions = self.gameData["directions"]
                        self.drillLevels = self.gameData["drilllevels"]
                        self.drillprogression = self.gameData["drillProgression"]
                        self.conveyorTurns = self.gameData["conveyorTurns"]
                        self.pastTitle = True
                #creates new game
                elif updates == 2:
                    self.gameData = askLoad(2)
                    self.tileMap = self.gameData["tilemap"]
                    self.toplayer = self.gameData["toplayer"]
                    self.directions = self.gameData["directions"]
                    self.drillLevels = self.gameData["drilllevels"]
                    self.drillprogression = self.gameData["drillProgression"]
                    self.conveyorTurns = self.gameData["conveyorTurns"]
                    self.pastTitle = True
                mousex, mousey = pygame.mouse.get_pos()
                # screen.fill((0,0,0))
                screen.blit(pointer,(mousex, mousey))
                pygame.display.flip()
        self.createTileMap()
        self.createTopLayer()
        while self.running:
            self.relx, self.rely = pygame.mouse.get_rel()
            self.clock.tick(60)
            self.fpsdisplay = self.font.render(str(int(self.clock.get_fps())), False, (255,255,255))
            self.tilegroupvariables = self.tilegroup.sprites()
            self.weatherbrightness = self.stormHandler.getBrightness()
            self.Player.update()
            self.core.update(self.Player.x, self.Player.y)
            self.draw()
            
            self.stormHandler.loop()
            self.tilegroup.update(self.Player.x, self.Player.y, self.md, self)
            self.topgroup.update(self.Player.x, self.Player.y, self.mdel, self)
            self.conveyorgroup.update(self.Player.x, self.Player.y, self.frame, self.mdel, self)
            for a in self.itemgroup.sprites():
                a.checkahead(self.toplayer)
            self.itemgroup.update(self.Player.x, self.Player.y, self.toplayer, self.directions)

            if self.frame >= 4:
                self.frame = 1

            
            self.Speaker.update(self.biomeid)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.gameData["topLayer"] = self.toplayer
                    self.gameData["drillProgression"] = self.drillprogression
                    self.gameData["conveyorTurns"] = self.conveyorTurns
                    askSave(self.gameData)
                    self.running = False
                    sys.exit()
                    

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self.md = True
                    if pygame.mouse.get_pressed()[2]:
                        self.mdel = True

                if event.type == pygame.MOUSEBUTTONUP:
                        self.md = False
                        self.mdel = False

                


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.selection = 1

                    if event.key == pygame.K_2:
                        self.selection = 2
                        self.drillselection = 0
                
                    if event.key == pygame.K_3:
                        self.selection = 2
                        if self.drillprogression >= 1:
                            self.drillselection = 1

                    if event.key == pygame.K_4:
                        self.selection = 2
                        if self.drillprogression >= 2:
                            self.drillselection = 2

                    if event.key == pygame.K_5:
                        self.selection = 3

                    if event.key == pygame.K_6:
                        self.selection = 4
                        

                    if event.key == pygame.K_r:
                        if self.tileclickdir >= 3:
                            self.tileclickdir = 0
                        else:
                            self.tileclickdir += 1

            
            self.passedframes += 1
            if self.passedframes >= 10:
                self.frame += 1
                self.passedframes = 0

                    
    def draw(self):
            # screen.fill((r,g,b))
            self.visableScreen.fill((0,0,0))
            self.weatherScreen.fill((0,0,0))

            self.stormHandler.draw(self.weatherScreen)
            self.weatherScreen.set_alpha(self.weatherbrightness)
            self.tilegroup.draw(self.visableScreen)
            self.topgroup.draw(self.visableScreen)
            self.conveyorgroup.draw(self.visableScreen)
            self.itemgroup.draw(self.visableScreen)
            self.core.draw(self.visableScreen)

            mx, my = pygame.mouse.get_pos()

            self.Player.draw(self.visableScreen)
            self.visableScreen.blit(self.weatherScreen, (0,0), (0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
            screen.blit(self.visableScreen, (0,0), (0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
            screen.blit(pointer,(mx, my))
            screen.blit(self.fpsdisplay, (0,0))
            pygame.display.flip()



    def createTileMap(self):
        for i, row in enumerate(self.tileMap):
            for j, column in enumerate(row):
                if column == 0:
                    t = Ground(self, i, j, self.biomeid)
                    self.tilegroup.add(t)
                if column == 1:
                    t = CopperOre(self, i, j, self.biomeid)
                    self.tilegroup.add(t)
                if column == 2:
                    t = IronOre(self, i, j, self.biomeid)
                    self.tilegroup.add(t)
                if column == 3:
                    t = Stone(self, i, j, self.biomeid)
                    self.tilegroup.add(t)
                if column == 4:
                    t = CoalOre(self, i, j, self.biomeid)
                    self.tilegroup.add(t)
                if column == 5:
                    t = TitaniumOre(self, i, j, self.biomeid)
                    self.tilegroup.add(t)
                if column == 6:
                    t = LeadOre(self, i, j, self.biomeid)
                    self.tilegroup.add(t)
                if column == 7:
                    t = UraniumOre(self, i, j, self.biomeid)
                    self.tilegroup.add(t)
                if column == 8:
                    t = ThoriumOre(self, i, j, self.biomeid)
                    self.tilegroup.add(t)
        self.core = Core(self.corex, self.corey)

    def createTopLayer(self):
        for ti, trow in enumerate(self.toplayer):
            for tj, tcolumn in enumerate(trow):
                if tcolumn == 1:
                    c = Conveyor(self, ti, tj, self.directions[ti][tj])
                    self.conveyorgroup.add(c)
                if tcolumn == 2:
                    d = Drill(self, ti, tj, self.drillLevels[ti][tj], self.tileMap[ti][tj])
                    self.topgroup.add(d)

    def clickedTile(self, clickx, clicky):
        self.clickx = clickx
        self.clicky = clicky
        #self.Speaker.placeSound()
        for a in self.itemgroup.sprites():
            a.look(self.toplayer, self.directions)
        if self.toplayer[clickx, clicky] == 0:
            if self.selection == 1:

                c = Conveyor(self, self.clickx, self.clicky, self.tileclickdir)
                self.conveyorgroup.add(c)

                self.toplayer[int(clickx)][int(clicky)] = self.selection
                self.directions[clickx][clicky] = self.tileclickdir
                for s in self.conveyorgroup.sprites():
                        dat, ax, sy = s.checkProx(self.toplayer, self.directions, self.conveyorTurns)
                        self.conveyorTurns[ax][sy] = dat


            if self.selection == 2:

                above = self.tileMap[clickx][clicky]
                d = Drill(self, self.clickx, self.clicky, self.drillselection, above)
                self.topgroup.add(d)
                self.toplayer[int(clickx)][int(clicky)] = self.selection
                self.drillLevels[clickx][clicky] = self.drillselection

            if self.selection == 3:
                n = Powernode(self, self.clickx, self.clicky)
                self.topgroup.add(n)
                self.toplayer[int(clickx)][int(clicky)] = self.selection

            if self.selection == 4:
                n = Battery(self, self.clickx, self.clicky)
                self.topgroup.add(n)
                self.toplayer[int(clickx)][int(clicky)] = self.selection




    def deleteTile(self, clickx, clicky):
        self.Speaker.delSound()
        self.toplayer[int(clickx)][int(clicky)] = 0
        for s in self.conveyorgroup.sprites():
            dat, ax, sy = s.checkProx(self.toplayer, self.directions, self.conveyorTurns)
            self.conveyorTurns[ax][sy] = dat

    def createItem(self, x, y, extracting):
        if extracting == 0:
            a = copperItem(x, y, 0)
        elif extracting == 1:
            a = ironItem(x, y, 0)
        elif extracting == 2:
            a = stoneItem(x, y, 0)
        elif extracting == 3:
            a = coalItem(x, y, 0)
        elif extracting == 4:
            a = titaniumItem(x, y, 0)
        elif extracting == 5:
            a = leadItem(x, y, 0)
        elif extracting == 6:
            a = uraniumItem(x, y, 0)
        elif extracting == 7:
            a = thoriumItem(x, y, 0)
        elif extracting == 8:
            a = thoriumItem(x, y, 0)
        else:
            a = thoriumItem(x, y, 0)
        self.itemgroup.add(a)

gameobj = main()
