import pygame as pg
from animal import animal
import random as rnd
import json

with open('para.json', 'r') as para:
    config = json.load(para)

class wolf(animal):
    def __init__(self, surface, index, posx, posy, movementspeed, sense, den):
        animal.__init__(self, surface, index, posx, posy, movementspeed, sense, den)
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
        self.travelLocation = None

    def travelToNextDen(self, wolfDens):
        if self.travelLocation:
            velocity = self.createVelocity(self.travelLocation)
            self.oldPosition = self.getPosition()
            self.oldCenter = self.rect.center
            self.rect.left = (self.rect.left + velocity[0]) % 800
            self.rect.top = (self.rect.top + velocity [1]) % 800

            if self.travelLocation == self.getPosition():
                self.travelLocation = None
        elif self.travelLocation == None:
            dens = list(wolfDens)
            dens.remove(self.den)
            travelLocation = rnd.choice(dens)
            self.travelLocation = travelLocation.getPosition()
            self.travelToNextDen(wolfDens)

    def followKnowledge(self):
        velocity = self.createVelocity(self.knowledge)

        self.oldPosition = self.getPosition()
        self.oldCenter = self.rect.center
        self.rect.left = (self.rect.left + velocity[0]) % 800
        self.rect.top = (self.rect.top + velocity [1]) % 800

        if self.knowledge == self.getPosition():
            self.knowledge = None

    def wander(self, wolfDens):
            if self.knowledge:
                self.followKnowledge()
            else:
                self.travelToNextDen(wolfDens)

    def move(self, indexMap, objectsDictionary, wolfDens):
        if self.wandering == True:
            self.wander(wolfDens)
            self.seek(indexMap, objectsDictionary)

        elif self.wandering == False:
            if self.target.dead == False:
                velocity = self.createVelocity(self.target.getPosition())
                if velocity[0] == 0 and velocity[1] == 0:
                    self.wandering = True
                    self.wander(wolfDens)
                else:
                    self.oldPosition = self.getPosition()
                    self.oldCenter = self.rect.center
                    self.rect.left = (self.rect.left + velocity[0]) % 800
                    self.rect.top = (self.rect.top + velocity [1]) % 800
                
            elif self.target.dead == True:
                self.wandering = True
                self.wander(wolfDens)
            
        self.energy -= self.ms