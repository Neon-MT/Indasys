import pygame
import random
import numpy as np
import pickle
pygame.init()

TILESIZE = 100

SCREEN_WIDTH=pygame.display.Info().current_w
SCREEN_HEIGHT=pygame.display.Info().current_h #subtract 50 if not in fullscreen

WINDOWRECT = pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
PLANET = 2
DIFFICULTY = 1000

MOVEMENTSPEED = 6
MAPSIZE = 50
DEFAULT = np.array ([[0 for x in range(MAPSIZE)] for y in range(MAPSIZE)])
TOPLAYER = np.array([[0 for x in range(MAPSIZE)]for y in range(MAPSIZE)])
DIRECTIONS = np.array([[9 for x in range(MAPSIZE)]for y in range(MAPSIZE)])
LEVELS = np.array([[9 for x in range(MAPSIZE)]for y in range(MAPSIZE)])
CONVEYORTURNS = np.array([[9 for x in range(MAPSIZE)]for y in range(MAPSIZE)])

def getMiddle():
    w, h = pygame.display.get_surface().get_size()
    SCREEN_MIDDLE_X = w / 2
    SCREEN_MIDDLE_Y = h / 2
    return SCREEN_MIDDLE_X, SCREEN_MIDDLE_Y


class loader():
    # Makes a 10x10 cluster with a higher chance to spawn on the inside rather than on the outskirts
    def makeCluster(self, orevalue):
        CLUSTERVALUES = [[random.randint(1,5),random.randint(1,5),random.randint(1,5),random.randint(1,5),random.randint(1,5),random.randint(1,4)],
                        [random.randint(1,5),random.randint(1,3),random.randint(1,3),random.randint(1,3),random.randint(1,3),random.randint(1,5)],
                        [random.randint(1,5),random.randint(1,3),random.randint(1,2),random.randint(1,1),random.randint(1,3),random.randint(1,5)],
                        [random.randint(1,5),random.randint(1,3),random.randint(1,1),random.randint(1,2),random.randint(1,3),random.randint(1,5)],
                        [random.randint(1,5),random.randint(1,3),random.randint(1,3),random.randint(1,3),random.randint(1,3),random.randint(1,5)],
                        [random.randint(1,4),random.randint(1,5),random.randint(1,5),random.randint(1,5),random.randint(1,5),random.randint(1,6)],]
        
        CLUSTER = np.array([[0 for x in range(6)] for y in range(6)])

        for i,row in enumerate(CLUSTERVALUES):
            for j, column in enumerate(row):
                if column == 1:
                    CLUSTER[i][j] = orevalue
                else:
                    CLUSTER[i][j] = 0
        return CLUSTER


    def loadTileMap(self):
        #copper(1)
        copperChance = 450 + DIFFICULTY
        COPPERCLUSTERSPAWN = ([[random.randint(1,copperChance) for x in range(MAPSIZE)] for y in range(MAPSIZE)])

        for i,row in enumerate(COPPERCLUSTERSPAWN):
            for j, column in enumerate(row):
                if column == copperChance:
                    cluster = self.makeCluster(1)
                    try:
                        row_start, row_end = i, 6+i
                        col_start, col_end = j, 6+j
                        DEFAULT[row_start:row_end, col_start:col_end] = cluster
                    except:
                        pass
        
        #Iron(2)
        ironChance = 500+ DIFFICULTY
        IRONCLUSTERSPAWN = ([[random.randint(1,ironChance) for x in range(MAPSIZE)] for y in range(MAPSIZE)])

        for x,r in enumerate(IRONCLUSTERSPAWN):
            for y, cl in enumerate(r):
                if cl == ironChance:
                    c = self.makeCluster(2)
                    try:
                        row_start, row_end = x, 6+x
                        col_start, col_end = y, 6+y
                        DEFAULT[row_start:row_end, col_start:col_end] = c
                    except:
                        pass
        
        #Stone(3)
        stoneChance = 100 + DIFFICULTY
        STONECLUSTERSPAWN = ([[random.randint(1,stoneChance) for x in range(MAPSIZE)] for y in range(MAPSIZE)])

        for stonex,stoner in enumerate(STONECLUSTERSPAWN):
            for stoney, stonecl in enumerate(stoner):
                if stonecl == stoneChance:
                    stonec = self.makeCluster(3)
                    try:
                        row_start, row_end = stonex, 6+stonex
                        col_start, col_end = stoney, 6+stoney
                        DEFAULT[row_start:row_end, col_start:col_end] = stonec
                    except:
                        pass
        
        #Coal(4)
        CoalChance = 300 + DIFFICULTY
        COALCLUSTERSPAWN = ([[random.randint(1,CoalChance) for x in range(MAPSIZE)] for y in range(MAPSIZE)])

        for Coalx,Coalr in enumerate(COALCLUSTERSPAWN):
            for Coaly, Coall in enumerate(Coalr):
                if Coall == CoalChance:
                    Coalc = self.makeCluster(4)
                    try:
                        row_start, row_end = Coalx, 6+Coalx
                        col_start, col_end = Coaly, 6+Coaly
                        DEFAULT[row_start:row_end, col_start:col_end] = Coalc
                    except:
                        pass

        #Titanium(5)
        TitaniumChance = 500 + DIFFICULTY
        TITANIUMCLUSTERSPAWN = ([[random.randint(1,TitaniumChance) for x in range(MAPSIZE)] for y in range(MAPSIZE)])

        for Titaniumx,Titaniumr in enumerate(TITANIUMCLUSTERSPAWN):
            for Titaniumy, Titaniuml in enumerate(Titaniumr):
                if Titaniuml == TitaniumChance:
                    Titaniumc = self.makeCluster(5)
                    try:
                        row_start, row_end = Titaniumx, 6+Titaniumx
                        col_start, col_end = Titaniumy, 6+Titaniumy
                        DEFAULT[row_start:row_end, col_start:col_end] = Titaniumc
                    except:
                        pass
        
        #Lead(6)
        LeadChance = 500 + DIFFICULTY
        LEADCLUSTERSPAWN = ([[random.randint(1,LeadChance) for x in range(MAPSIZE)] for y in range(MAPSIZE)])

        for Leadx,Leadr in enumerate(LEADCLUSTERSPAWN):
            for Leady, Leadl in enumerate(Leadr):
                if Leadl == LeadChance:
                    Leadc = self.makeCluster(6)
                    try:
                        row_start, row_end = Leadx, 6+Leadx
                        col_start, col_end = Leady, 6+Leady
                        DEFAULT[row_start:row_end, col_start:col_end] = Leadc
                    except:
                        pass
        
        #Uranium(7)
        UraniumChance = 500 + DIFFICULTY
        URANIUMCLUSTERSPAWN = ([[random.randint(1,UraniumChance) for x in range(MAPSIZE)] for y in range(MAPSIZE)])

        for Uraniumx,Uraniumr in enumerate(URANIUMCLUSTERSPAWN):
            for Uraniumy, Uraniuml in enumerate(Uraniumr):
                if Uraniuml == UraniumChance:
                    Uraniumc = self.makeCluster(7)
                    try:
                        row_start, row_end = Uraniumx, 6+Uraniumx
                        col_start, col_end = Uraniumy, 6+Uraniumy
                        DEFAULT[row_start:row_end, col_start:col_end] = Uraniumc
                    except:
                        pass

        #Thorium(8)
        ThoriumChance = 900 + DIFFICULTY
        THORIUMCLUSTERSPAWN = ([[random.randint(1,ThoriumChance) for x in range(MAPSIZE)] for y in range(MAPSIZE)])

        for Thoriumx,Thoriumr in enumerate(THORIUMCLUSTERSPAWN):
            for Thoriumy, Thoriuml in enumerate(Thoriumr):
                if Thoriuml == ThoriumChance:
                    Thoriumc = self.makeCluster(8)
                    try:
                        row_start, row_end = Thoriumx, 6+Thoriumx
                        col_start, col_end = Thoriumy, 6+Thoriumy
                        DEFAULT[row_start:row_end, col_start:col_end] = Thoriumc
                    except:
                        pass

        returnr = {"tilemap":DEFAULT, "toplayer":TOPLAYER, "mapsize":MAPSIZE, "directions":DIRECTIONS, "drilllevels":LEVELS, "drillProgression":0, "conveyorTurns":CONVEYORTURNS, "planet":PLANET}
        return returnr


    def loadsave(self):
        with open("save.dat", 'rb') as f:
            self.loadedgame = pickle.load(f)
        f.close()
        return self.loadedgame



class save():
    def __init__(self):
        pass

    def savegame(self, gamedata):
        with open("save.dat", "wb") as f:
            pickle.dump(gamedata, f)
        f.close()
        
