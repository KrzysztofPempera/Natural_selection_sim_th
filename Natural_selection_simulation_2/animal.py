import pygame as pg
import random as rnd
import numpy as np
import math
import json


with open('para.json', 'r') as para:
    config = json.load(para)


MUTATION_THRESHOLD = 0.5

class animal(object):
    
    def __init__(self, surface, index, posx, posy, movementspeed, sense, den):
        self.surface = surface
        self.index = index
        self.sense = sense
        self.ms = movementspeed

        self.dead = False
        self.eat = False
        self.wandering = True
        self.velocity = (0,0)
        self.target = object
        self.oldPosition = (-1,-1)
        self.oldCenter = (-1,-1)
        self.age = 0
        self.knowledge = ()
        self.den = den
        self.eaten = []


    def getPosition(self):
        return self.rect.left, self.rect.top

    def normalize(self, v):
        norm = np.linalg.norm(v)
        if norm == 0:
            print("0 norm exception")
            return v
        return v / norm

    def calcDistance(self, a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def createVelocity(self, target):
        animalPosition = self.getPosition()
        targetPosition = target.getPosition()

        desired = np.subtract(targetPosition, animalPosition)

        dCheck = math.ceil(math.sqrt((desired[0]**2)+(desired[1]**2)))

        desired = self.normalize(desired)
        desired = desired * self.ms
        desired = (math.floor(desired[0]) if desired[0] < 0 else math.ceil(desired[0]) ,math.floor(desired[1]) if desired[1] < 0 else math.ceil(desired[1]))

        if dCheck > 400:
            return np.negative(desired)
        elif dCheck <= self.ms or dCheck <= 1:
            return np.subtract(targetPosition, animalPosition)
        else:
            return desired

    def mutate(self, parameter):
        mutationPosibilities = [1,-1]
        ifMutate = rnd.uniform(0,1)

        if ifMutate < MUTATION_THRESHOLD:   
            parameter += rnd.choice(mutationPosibilities)
        return parameter

    def reproduce(self, referenceList, animal, objectsIndex, objectsDictionary):
        self.energy = math.floor(self.energy*config['REPRODUCTION_COST'])
        aPosition = self.den.getPosition()

        newMs = self.mutate(self.ms)
        newSense = self.mutate(self.sense)

        if newSense <=10:
            newSense = 11
        if newMs <= 0:
            newMs = 1
        
        newIndex = self.type + str(objectsIndex)
        newAnimal = animal(self.surface,newIndex,  aPosition[0], aPosition[1], newMs, newSense, self.den)
        referenceList.append(newAnimal)
        objectsDictionary[newAnimal.index] = newAnimal


    def search(self, indexMap):
        center = self.rect.center
        sense = self.sense
        target = 'g'
        #topleft - topright
        for i in range((center[0] - sense) % 800, (center[0] + sense) % 800):
            x = i % 800
            y = (center[1] - sense) % 800
            if indexMap[y][x][0] == self.prey:
                target = indexMap[y][x]
                return target
        #topright - bottomright
        for i in range((center[1] - sense) % 800, (center[1] + sense) % 800):
            x = (center[0] + sense) % 800
            y = i % 800
            if indexMap[y][x][0] == self.prey:
                target = indexMap[y][x]
                return target
        #bottomright - bottomleft
        for i in range((center[0] + sense) % 800, (center[0] - sense) % 800, -1):
            x = i % 800
            y = (center[1] + sense) % 800
            if indexMap[y][x][0] == self.prey:
                target = indexMap[y][x]
                return target
        #bottomleft - topleft
        for i in range ((center[1] - sense) % 800, (center[1] + sense) % 800):
            x = (center[0] - sense) % 800
            y = i % 800
            if indexMap[y][x][0] == self.prey:
                target = indexMap[y][x]
                return target



        return target

    def seek(self, indexMap, objectsDictionary):
        target = self.search(indexMap)
        if target[0] == self.prey:
            self.target = objectsDictionary.get(target)
            self.wandering = False
        else:
            self.wandering = True

    def selfScan(self, indexMap):
        x = self.rect.left
        y = self.rect.top
        h = self.rect.h

        #scanningArea = [(self.rect.left, self.rect.top), (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.top), (self.rect.right, self.rect.bottom), 
        #                (self.rect.left + int(h/2), self.rect.top), (self.rect.left + int(h/2), self.rect.bottom), (self.rect.left, self.rect.top - int(h/2)),
        #               (self.rect.right, self.rect.top  - int(h/2)), (self.rect.center)]
        
        #for area in scanningArea:
        #    if indexMap[area[1]%800][area[0]%800][0] == self.prey:
        #        return indexMap[area[1]%800][area[0]%800]

        for i in range(y, (y + h + 1) % 800):
            for j in range(x, (x + h +1) % 800):
                if indexMap[i][j][0] == self.prey:
                    return indexMap[i][j]
        return 'g'

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
            self.oldCenter = self.rect.center
            return newPosition
        else:
            return self.wanderingDirection()

    def wander(self):
            newPosition = self.wanderingDirection()
            self.rect.left = newPosition[0] % 800
            self.rect.top = newPosition[1] % 800
    
    def findClosestDen(self, dens):
        closest = self.calcDistance(self.getPosition(), self.den.getPosition())
        for den in dens:
            n = self.calcDistance(self.getPosition(), den.getPosition())
            if n < closest:
                closest = n
                self.den = den

    def moveBackToDen(self, bg):
        velocity = self.createVelocity(self.den)

        self.oldPosition = self.getPosition()
        self.oldCenter = self.rect.center
        self.rect.left = (self.rect.left + velocity[0]) % 800
        self.rect.top = (self.rect.top + velocity [1]) % 800
        self.surface.blit(bg, (self.oldPosition[0], self.oldPosition[1]))


    def move(self, bg, indexMap, objectsDictionary):
        if self.wandering == True:
            self.wander()
            self.seek(indexMap, objectsDictionary)

        elif self.wandering == False:
            if self.target.dead == False:
                velocity = self.createVelocity(self.target)
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
            
        self.surface.blit(bg, (self.oldPosition[0], self.oldPosition[1]))
        self.energy -= self.ms
                        