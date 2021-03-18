import random as  rnd
import pygame as pg
import numpy as np
import math

class den(object):

    def __init__(self, posx, posy, image):

        self.posx = posx
        self.posy = posy
        self.image = pg.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy
        self.animals = []

    def getPosition(self):
        return self.posx, self.posy

    def __normalize(self, v):
        norm = np.linalg.norm(v)
        if norm == 0:
            print("0 norm exception")
            return v
        return v / norm

    def __calcDistance(self, a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def __createVelocity(self, targetPosition, startPosition):

        desired = np.subtract(targetPosition, startPosition)
        desired = self.__normalize(desired)
        desired = (math.floor(desired[0]) if desired[0] < 0 else math.ceil(desired[0]) ,math.floor(desired[1]) if desired[1] < 0 else math.ceil(desired[1]))
        return desired

    def __createPath(self, destination):
        path = []
        currentPosition = self.getPosition()
        while currentPosition != destination:
            velocity = self.__createVelocity(destination, currentPosition)
            newPosition = (currentPosition[0] + velocity[0],currentPosition[1] + velocity[1])
            currentPosition = newPosition
            path.append(currentPosition)
        return path

    def __calculatePathValue(self, path, traceMap):
        value = 0
        for coordinate in path:
            value += traceMap[coordinate[0]][coordinate[1]]
        return value

    def __bestPath(self, paths):
        best = paths[0][-1]
        bestPath = paths[0]
        for path in paths:
            if path[-1] < best:
                best = path[-1]
                bestPath = path
        return bestPath

    def __findBestPaths(self, arAnimals, traceMap):
        if arAnimals:
            paths = []
            for animal in arAnimals:
                if animal.eaten:
                    lastLocation = animal.eaten[-1]
                    path = self.__createPath(lastLocation)
                    pathValue = self.__calculatePathValue(path, traceMap)
                    path.append(pathValue)
                    paths.append(path)
            if len(paths) >0:
                bestPath = self.__bestPath(paths)
                return bestPath
            else:
                return None
        else:
            return None

    def shareKnowledge(self, traceMap, pathMap):
        bestPath = self.__findBestPaths(self.animals, traceMap)
        if bestPath:
            for coordinate in bestPath[:-1]:
                pathMap[coordinate[0]][coordinate[1]] = bestPath[-1]

            

    def clearDen(self):
        self.animals.clear()