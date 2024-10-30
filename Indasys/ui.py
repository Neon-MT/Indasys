import pygame
import sys
import thorpy as tp
from configLoader import *
import pygame.font


class titleScreen():
    def __init__(self):
        self.font = pygame.font.SysFont('Ariel', 50)
        self.titfont = pygame.font.SysFont('Protest Strike', 300)
        self.errfont = pygame.font.SysFont('Protest Strike', 300)
        self.midx, self.midy = getMiddle()
        self.loadsavedgameRect = pygame.Rect(self.midx-300,self.midy-150, 600,100)
        self.loadnewgameRect = pygame.Rect(self.midx-300,self.midy +150, 600,100)
        self.frames = 0
        self.passedframes = 0
        self.showerror = False

    def update(self, screen, returnerror):
        screen.fill((0,0,255))

        pygame.draw.rect(screen,(50,50,50), self.loadsavedgameRect)
        pygame.draw.rect(screen,(50,50,50), self.loadnewgameRect)
        self.text = self.font.render("Load Saved Game", False, (255,255,255))
        self.newgametext = self.font.render("Create new game", False, (255,255,255))
        self.loadingtext = self.font.render("Loading...", False, (255,255,255))
        self.tittext = self.titfont.render("Indasys", False, (255,255,255))
        screen.blit(self.text, (self.midx - self.text.get_width()/2,self.midy - 125))
        screen.blit(self.tittext, (self.midx -self.tittext.get_width()/2,self.midy - 400))
        screen.blit(self.newgametext, (self.midx - self.newgametext.get_width()/2, self.midy +175))
        for ev in pygame.event.get(): 
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if self.loadsavedgameRect.collidepoint(mx,my):
                    screen.blit(self.loadingtext, (0,0))
                    return 1
                
                elif self.loadnewgameRect.collidepoint(mx,my):
                    screen.blit(self.loadingtext, (0,0))
                    return 2
                
        if returnerror:
            self.errtext = self.errfont.render("No save file found!", False, (255,0,0))
            self.showerror = True


        if self.showerror:
            self.passedframes += 1

            if self.passedframes >= 300:
                self.passedframes = 0
                self.showerror = False
            screen.blit(self.errtext, (0,0))

        self.frames +=1
        return 0      
    



class ui():
    def __init__(self, screen):
        self.screen = screen


    def update(self):
        pass
