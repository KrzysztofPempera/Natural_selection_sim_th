import pygame as pg
from animal import animal
import json

with open('para.json', 'r') as para:
    config = json.load(para)

class rabbit(animal):

    def __init__(self, surface, index, posx, posy, movementspeed, sense):
        animal.__init__(self, surface, index, movementspeed, sense)
        self.image = pg.image.load('Rabbit.png').convert()
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy

        self.type = 'r'
        self.prey = 'c'
        self.dead = False
        self.energy = config['RABBIT_ENERGY']
        self.maxEnergy = config['RABBIT_MAX_ENERGY']
        self.energyRep = config['RABBIT_ENERGY_REP']
        self.reproduciton = config['RABBIT_REPRODUCTION']
        self.den = (posx, posy)
        