import pygame as pg
from animal import animal

class rabbit(animal):

    def __init__(self, surface, index, posx, posy, movementspeed, sense):
        animal.__init__(self, surface, index, movementspeed, sense)
        self.image = pg.image.load('Rabbit.png').convert()
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy

        self.dead = False
        self.energy = 150
        self.maxEnergy = 500
        self.energyRep = 20
        self.reproduciton = 0.2
        