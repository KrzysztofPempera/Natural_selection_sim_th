import pygame as pg
import random as rnd
import numpy as np
import math

class animal(object):
    
    def __init__(self, surface, index, movementspeed, sense):
        self.surface = surface
        self.index = index
        self.sense = sense
        self.ms = movementspeed

        self.eat = False
        self.wandering = False
        self.velocity = (0,0)
        self.target = True
        self.oldPosition = (-1,-1)
        self.age = 0
        self.family = -1

    def getPosition(self):
        return self.rect.left, self.rect.top

    def normalize(self, v):
        norm = np.linalg.norm(v)
        if norm == 0:
            print("0 norm exception")
            return v
        return v / norm

    def createVelocity(self):
        animalPosition = self.getPosition()
        targetPosition = (2,3)

        desired = np.subtract(targetPosition, animalPosition)

        desired = self.normalize(desired)
        desired = desired * self.ms
        velocity = (math.ceil(desired[0]),math.ceil(desired[1]))
        return velocity

    def getNewPosition(self, position):
        moves = ((0,self.ms),(0,-self.ms),(self.ms,0),(-self.ms,0), (self.ms,self.ms), (self.ms,-self.ms), (-self.ms,self.ms), (-self.ms,-self.ms))
        nextMove = moves[rnd.randrange(len(moves))]

        newPosition = (position[0] + nextMove[0],position[1] + nextMove[1])
        return newPosition

    def wanderingDirection(self):
        position = self.getPosition()
        newPosition = self.getNewPosition(position)
        if newPosition != self.oldPosition:
            self.oldPosition = position
            return newPosition
        else:
            return self.wanderingDirection()

    def wander(self):
            newPosition = self.wanderingDirection()
            self.rect.left = newPosition[0] % 500
            self.rect.top = newPosition[1] % 500

    def move(self, bg):
        if self.wandering == True:
            self.wander()

        elif self.wandering == False:
            if self.target == True:
                velocity = self.createVelocity()
                if velocity[0] == 0 and velocity[1] == 0:
                    self.wandering = True
                    self.wander()
                else:
                    self.oldPosition = self.getPosition()
                    self.rect.left = (self.rect.left + velocity[0]) % 500
                    self.rect.top = (self.rect.top + velocity [1]) % 500
                
            elif self.target == True:
                self.wandering = True
                self.wander()
            
        self.surface.blit(bg, (self.oldPosition[0], self.oldPosition[1]))
        self.energy -= self.ms
                        