import pygame as pg
import random as rnd
import numpy as np
import math
import json

with open('para.json', 'r') as para:
    config = json.load(para)


MUTATION_THRESHOLD = 0.5

class animal(object):
    
    def __init__(self, surface, index, movementspeed, sense):
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
        targetPosition = self.target.getPosition()

        desired = np.subtract(targetPosition, animalPosition)

        desired = self.normalize(desired)
        desired = desired * self.ms
        velocity = (math.ceil(desired[0]),math.ceil(desired[1]))
        return velocity

    def mutate(self, parameter):
        mutationPosibilities = [1,-1]
        ifMutate = rnd.uniform(0,1)

        if ifMutate < MUTATION_THRESHOLD:   
            parameter += rnd.choice(mutationPosibilities)
        return parameter

    def reproduce(self, referenceList, animal, objectsIndex, objectsDictionary):
        self.energy = math.floor(self.energy*config['REPRODUCTION_COST'])
        aPosition = self.getPosition()

        newMs = self.mutate(self.ms)
        newSense = self.mutate(self.sense)

        if newSense <=10:
            newSense = 11
        if newMs <= 0:
            newMs = 1
        
        newIndex = self.type + str(objectsIndex)
        newAnimal = animal(self.surface,newIndex,  aPosition[0], aPosition[1], newMs, newSense)
        referenceList.append(newAnimal)
        objectsDictionary[newAnimal.index] = newAnimal


    def search(self, indexMap):
        center = self.rect.center
        sense = self.sense
        target = 'g'
        ##to fix diferent species, function, around the world chase?
        #topleft - topright
        for i in range((center[0] - sense) % 500, (center[0] + sense) % 500):
            x = i % 500
            y = (center[1] - sense) % 500
            if indexMap[y][x][0] == self.prey:
                target = indexMap[y][x]
                return target
        #topright - bottomright
        for i in range((center[1] - sense) % 500, (center[1] + sense) % 500):
            x = (center[0] + sense) % 500
            y = i % 500
            if indexMap[y][x][0] == self.prey:
                target = indexMap[y][x]
                return target
        #bottomright - bottomleft
        for i in range((center[0] + sense) % 500, (center[0] - sense) % 500, -1):
            x = i % 500
            y = (center[1] + sense) % 500
            if indexMap[y][x][0] == self.prey:
                target = indexMap[y][x]
                return target
        #bottomleft - topleft
        for i in range ((center[1] - sense) % 500, (center[1] + sense) % 500):
            x = (center[0] - sense) % 500
            y = i % 500
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

        for i in range(y, (y + h + 1) % 500):
            for j in range(x, (x + h +1) % 500):
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
            return newPosition
        else:
            return self.wanderingDirection()

    def wander(self):
            newPosition = self.wanderingDirection()
            self.rect.left = newPosition[0] % 500
            self.rect.top = newPosition[1] % 500
    

    def move(self, bg, indexMap, objectsDictionary):
        if self.wandering == True:
            self.wander()
            self.seek(indexMap, objectsDictionary)

        elif self.wandering == False:
            if self.target.dead == False:
                velocity = self.createVelocity()
                if velocity[0] == 0 and velocity[1] == 0:
                    self.wandering = True
                    self.wander()
                else:
                    self.oldPosition = self.getPosition()
                    self.rect.left = (self.rect.left + velocity[0]) % 500
                    self.rect.top = (self.rect.top + velocity [1]) % 500
                
            elif self.target.dead == True:
                self.wandering = True
                self.wander()
            
        self.surface.blit(bg, (self.oldPosition[0], self.oldPosition[1]))
        self.energy -= self.ms
                        