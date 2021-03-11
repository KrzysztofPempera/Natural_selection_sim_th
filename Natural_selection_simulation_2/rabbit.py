import pygame as pg
from animal import animal
import json
import math

with open('para.json', 'r') as para:
    config = json.load(para)

class rabbit(animal):

    def __init__(self, surface, index, posx, posy, movementspeed, sense, den):
        animal.__init__(self, surface, index, posx, posy, movementspeed, sense, den)
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
        self.threatSense = 30
        self.danger = False
        self.threat = object
    
    def findHideout(self, dens, threat):
        closest = self.calcDistance(self.getPosition(), self.den.getPosition())
        hideout = self.den
        for den in dens:
            n = self.calcDistance(self.getPosition(), den.getPosition())
            if n < closest:
                closest = n
                hideout = den
        return hideout                

    def move(self, indexMap, objectsDictionary, wolfDens, rabbitDens):
        ms = math.ceil(self.ms * self.debuff)

        if self.danger == True:
            hideout = self.findHideout(rabbitDens, self.threat)
            if self.getPosition() == hideout.getPosition():
                self.hidden = True
                self.danger = False
                return
            velocity = self.createVelocity(hideout.getPosition())

            self.oldPosition = self.getPosition()
            self.oldCenter = self.rect.center
            self.rect.left = (self.rect.left + velocity[0]) % 800
            self.rect.top = (self.rect.top + velocity [1]) % 800

        elif self.wandering == True:
            self.wander()
            self.seek(indexMap, objectsDictionary)

        elif self.wandering == False:
            if self.target.dead == False:
                velocity = self.createVelocity(self.target.getPosition())
                if velocity[0] == 0 and velocity[1] == 0:
                    self.wandering = True
                    self.wander()
                else:
                    self.oldPosition = self.getPosition()
                    self.oldCenter = self.rect.center
                    self.rect.left = (self.rect.left + velocity[0]) % 800
                    self.rect.top = (self.rect.top + velocity [1]) % 800
                
            elif self.target.dead == True:
                self.wandering = True
                self.wander()
            
        self.energy -= ms
                        