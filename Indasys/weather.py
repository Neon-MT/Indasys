import pygame
import os
import random
import math
from particle import *
from configLoader import *
from sounds import *

class stormHandler(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.clouds = pygame.sprite.Group()
        self.rain = pygame.sprite.Group()
        self.a = 0

    def thunderStorm(self, intensity, duration):
        self.duration = duration
        self.setduration = duration
        self.intensity = intensity
        self.wind = self.intensity * 2
        self.x = 0
        a = particle(0,0,100,intensity,intensity, (40,40,40))
        self.clouds.add(a)
        

    def update(self):
        self.duration -= 1
        for e in range(self.intensity):
            if e % 5 == 0:
                colorvar = random.randint(-10,10)
                if random.randint(1,2) == 1:
                    a = particle(random.randint(0,SCREEN_WIDTH),-200,200, self.intensity+random.randint(-2,2), self.intensity+random.randint(-2,2), (40+colorvar,40+colorvar,40+colorvar))
                else:
                    a = particle(-200,random.randint(0,SCREEN_WIDTH),200, self.intensity+random.randint(-2,2), self.intensity+random.randint(-2,2), (40+colorvar,40+colorvar,40+colorvar))
                self.clouds.add(a)
            if e % 2 == 0:
                colorvar = random.randint(-10,10)
                if random.randint(1,2) == 1:
                    r = rain(random.randint(0,SCREEN_WIDTH),-200-self.wind,20, 50, self.wind, (0,0,255))
                else:
                    r = rain(-200,random.randint(0,SCREEN_WIDTH), 20, 50, self.wind, (0,0,255))
                self.rain.add(r)
            e += 1



        for c in self.clouds.sprites():
            c.move()
        for r in self.rain.sprites():
            r.move()
    
    def loop(self):
        if self.duration > 0:
            self.update()

    def draw(self, screen):
        for c in self.clouds.sprites():
            c.drawself(screen)
        for r in self.rain.sprites():
            r.drawself(screen)

    def getBrightness(self):
        
        self.x += 1
        if self.a <= 120:
            self.a = self.x
        if self.duration <= 120:
            self.a = self.duration
        return self.a
    

