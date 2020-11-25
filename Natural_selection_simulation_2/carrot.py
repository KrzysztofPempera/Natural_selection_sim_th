import random as rnd
import pygame as pg

class carrot(object):

    def __init__(self, surface, index, minX, maxX, minY, maxY):
        self.surface = surface
        self.energyRep = 50
        self.dead = False
        self.image = pg.image.load('Carrot.png').convert()
        self.rect = self.image.get_rect()
        self.index = index

        self.startingLocation = (rnd.randint(minX, maxX -1),rnd.randint(minY, maxY -1))
        self.rect.left, self.rect.top = self.startingLocation
        
    def getPosition(self):
        return self.rect.left, self.rect.top

        
