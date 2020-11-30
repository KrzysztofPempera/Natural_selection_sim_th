import pygame as pg
from animal import animal
import json

with open('para.json', 'r') as para:
    config = json.load(para)

class wolf(animal):
    def __init__(self, surface, index, posx, posy, movementspeed, sense):
        animal.__init__(self, surface, index, movementspeed, sense)
        self.image = pg.image.load('Wolf.png').convert()
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy

        self.type = 'w'
        self.prey = 'r'
        self.dead = False
        self.energy = config['WOLF_ENERGY']
        self.maxEnergy = config['WOLF_MAX_ENERGY']
        self.reproduciton = config['WOLF_REPRODUCTION']
        self.maxAge = config['WOLF_MAX_AGE']
        


