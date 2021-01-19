import random as  rnd
import pygame as pg

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

    def __findFittest(self, arAnimals):
        if arAnimals:
            alpha = arAnimals[0]
            maxEaten = len(arAnimals[0].eaten)

            for animal in arAnimals:
                if len(animal.eaten) > maxEaten:
                    maxEaten = len(animal.eaten)
                    alpha = animal
            return alpha
        else:
            return None
            

    def __createHuntingGrounds(self, animal):
        lastLocations = animal.eaten[-3:]
        return lastLocations

    def shareKnowledge(self):
        fittest = self.__findFittest(self.animals)
        if fittest and fittest.eaten:
            huntingGrounds = self.__createHuntingGrounds(fittest)
            for animal in self.animals:
                animal.knowledge =  rnd.choice(huntingGrounds)

    def clearDen(self):
        self.animals.clear()