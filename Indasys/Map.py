import pygame
from configLoader import *
import os

def askLoad(title):
    l = loader()
    #load saved game
    if title == 1:
        if os.path.exists('save.dat'):
            gdat = l.loadsave()
        else:
            return False
    #load new game
    if title == 2:
        gdat = l.loadTileMap()
        
    return gdat
    

def askSave(gamedata):
    asksave = input("Would you like to save your game? y/n")
    saver = save()
    if asksave == "y":
        saver.savegame(gamedata)