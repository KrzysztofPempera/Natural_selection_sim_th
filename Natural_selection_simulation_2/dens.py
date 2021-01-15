import random as  rnd

class den(object):

    def __init__(self, posx, posy):

        self.posx = posx
        self.posy = posy
        
        self.animals = []

    def getPosition(self):
        return self.posx, self.posy

    def findFittest(self, arAnimals):
        alpha = arAnimals[0]
        maxEaten = len(arAnimals[0].eaten)

        for animal in arAnimals:
            if len(animal.eaten) > maxEaten:
                maxEaten = len(animal.eaten)
                alpha = animal
        return alpha 

    def createHuntingGrounds(self, animal):
        lastLocations = animal.eaten[-3:]
        return lastLocations

    def shareKnowledge(self):
        fittest = self.fittest(animals)
        huntingGrounds = self.huntingGrounds(fittest)
        for animal in animals:
            animal.knowledge =  rnd.choice(huntingGrounds)