import pygame

class creature(pygame.sprite.Sprite):
    def __init__(self, x, y, type, color):
        self.x = x
        self.y = y 
        self.color = color

    def leg(self, end):
        return pygame.draw.line()

    def update(self):
        pass