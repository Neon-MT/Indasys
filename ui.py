import pygame
import sys
from configLoader import *
import pygame.font


class titleScreen():
    def __init__(self):
        self.font = pygame.font.SysFont('Cascadia Code', 50)
        self.titfont = pygame.font.SysFont('Impact', 300)
        self.errfont = pygame.font.SysFont('Protest Strike', 50)
        self.spacing = 200
        self.offset = 200
        self.midx, self.midy = getMiddle()
        self.loadsavedgameRect = pygame.Rect(self.midx-300,(self.spacing) + self.offset, 600,100)
        self.loadnewgameRect = pygame.Rect(self.midx-300,(2* self.spacing) + self.offset, 600,100)
        self.quitRect = pygame.Rect(self.midx-300,(3 * self.spacing) + self.offset, 600,100)
        self.frames = 0
        self.passedframes = 0
        self.showerror = False
        self.pr = 2
        self.pg = 2
        self.pb = 3
        self.fadein = True

    def update(self, screen, returnerror):
        if self.fadein:
            self.pr += 0.2
            self.pg += 0.2
            self.pb += 0.3
            if self.pb >= 50:
                self.fadein = False

        screen.fill((self.pr,self.pg,self.pb))

        pygame.draw.rect(screen,(50,50,50), self.loadsavedgameRect)
        pygame.draw.rect(screen,(50,50,50), self.loadnewgameRect)
        pygame.draw.rect(screen,(50,50,50), self.quitRect)
        self.text = self.font.render("Load Saved Game", False, (255,255,255))
        self.newgametext = self.font.render("Create new game", False, (255,255,255))
        self.loadingtext = self.font.render("Loading...", False, (255,255,255))
        self.quitgame = self.font.render("Quit", False, (255,255,255))
        self.tittext = self.titfont.render("I n d a s y s", True, (255,255,255))
        screen.blit(self.tittext, (self.midx -self.tittext.get_width()/2,self.midy - 550))
        screen.blit(self.text, (self.midx - self.text.get_width()/2,(self.spacing) + self.offset + self.loadsavedgameRect.height/2 - self.text.get_height()/2))
        screen.blit(self.newgametext, (self.midx - self.newgametext.get_width()/2, (2 * self.spacing) + self.offset + self.loadnewgameRect.height/2 - self.newgametext.get_height()/2))
        screen.blit(self.quitgame, (self.midx - self.quitgame.get_width()/2,(3 * self.spacing) + self.offset + self.quitRect.height/2 - self.quitgame.get_height()/2))
        mx, my = pygame.mouse.get_pos()
        for ev in pygame.event.get(): 
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if self.loadsavedgameRect.collidepoint(mx,my):
                    screen.blit(self.loadingtext, (0,0))
                    return 1
                
                elif self.loadnewgameRect.collidepoint(mx,my):
                    screen.blit(self.loadingtext, (0,0))
                    return 2
                elif self.quitRect.collidepoint(mx,my):
                    return 3
                
        if returnerror:
            self.errtext = self.errfont.render("No save file found!", False, (255,0,0))
            self.showerror = True


        if self.showerror:
            self.passedframes += 1

            if self.passedframes >= 300:
                self.passedframes = 0
                self.showerror = False
            screen.blit(self.errtext, (mx, my-25))

        self.frames +=1
        return 0      
    

class pausemenu():
    def __init__(self):
        self.midx, self.midy = getMiddle()
        self.spacing = 100
        self.widths = 300
        self.heights = 60
        self.offset = self.midy
        self.resumeRect = pygame.Rect(self.midx-self.widths/2, self.spacing + self.offset, self.widths, self.heights)
        self.font = pygame.font.SysFont('Cascadia Code', 50)
        self.pausedText = self.font.render("Paused",False, (255,255,255))
        self.resumeText = self.font.render("Resume",False, (255,255,255))

    
    def update(self, screen):
        pygame.draw.rect(screen, (50,50,50), self.resumeRect)
        screen.blit(self.pausedText, (self.midx-self.pausedText.get_width()/2, 10))
        screen.blit(self.resumeText, (self.midx-self.resumeText.get_width()/2, self.resumeRect.centery-self.resumeText.get_height()/2))


class ui():
    def __init__(self, screen):
        self.screen = screen


    def update(self):
        pass
