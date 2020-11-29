import random as rnd
import pygame as pg
import json

with open('para.json', 'r') as para:
    config = json.load(para)

class carrot(object):

    def __init__(self, surface, index, minX, maxX, minY, maxY):
        self.surface = surface
        self.energyRep = config['CARROT_ENERGY_REP']
        self.dead = False
        self.image = pg.image.load('Carrot.png').convert()
        self.rect = self.image.get_rect()
        self.index = index

        self.type = 'c'
        self.startingLocation = (rnd.randint(minX, maxX -1),rnd.randint(minY, maxY -1))
        self.rect.left, self.rect.top = self.startingLocation
        
    def getPosition(self):
        return self.rect.left, self.rect.top

        
