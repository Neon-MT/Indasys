import pygame # type: ignore
import math
import os
from configLoader import *
pygame.init()

class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        SCREEN_MIDDLE_X, SCREEN_MIDDLE_Y = getMiddle()
        self.x = (MAPSIZE*TILESIZE)/-2
        self.y = (MAPSIZE*TILESIZE)/-2
        self.x_vel = 0
        self.y_vel = 0
        self.image = pygame.image.load(os.path.dirname(__file__)+ "/assets/playerMain.png")
        self.image = pygame.transform.scale(self.image, (100,100))
        self.drawx = SCREEN_MIDDLE_X
        self.drawy =  SCREEN_MIDDLE_Y 

        self.rect = self.image.get_rect(center = (self.drawx, self.drawy))
        self.hitbox = self.image.get_rect()
        self.game = game
        self.rotation = 0


    def update(self):

        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.y += MOVEMENTSPEED

        if key[pygame.K_w] and key[pygame.K_LSHIFT]:
            self.y += MOVEMENTSPEED + 3

        if key[pygame.K_s]:
            self.y -= MOVEMENTSPEED 

        if key[pygame.K_s] and key[pygame.K_LSHIFT]:
            self.y -= MOVEMENTSPEED + 3

        if key[pygame.K_a]:
            self.x += MOVEMENTSPEED

        if key[pygame.K_a] and key[pygame.K_LSHIFT]:
            self.x += MOVEMENTSPEED + 3

        if key[pygame.K_d]:
            self.x -= MOVEMENTSPEED 

        if key[pygame.K_d] and key[pygame.K_LSHIFT]:
            self.x -= MOVEMENTSPEED + 3



        mouse_x, mouse_y = pygame.mouse.get_pos()



        try:
            angle = 360-math.atan2(mouse_x - self.drawx, mouse_y - self.drawy)*180/math.pi * -1 - 180
            #angle += self.image.get_width()
        except:
            angle = 0

        



        self.image2 = pygame.transform.rotozoom(self.image, int(angle), 1)
        self.rect = self.image2.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image2, self.rect)

    