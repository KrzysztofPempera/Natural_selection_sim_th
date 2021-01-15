import pygame as pg
import random as rnd
import sprites as sp
import carrot as crt
import rabbit as rb
import dens as dn 
import wolf as wlf
import sys
import numpy as np
import colours
import json

with open('para.json', 'r') as para:
    config = json.load(para)

WIDTH = 800
HEIGHT = 800
SPEED = 18
RABBIT_MOVEMENT_SPEED = config['RABBIT_MOVEMENT_SPEED']
WOLF_MOVEMENT_SPEED = config['WOLF_MOVEMENT_SPEED']
WOLF_SENSE = config['WOLF_SENSE']
RABBIT_SENSE = config['RABBIT_SENSE']
CARROT_REP = config['CARROT_REP']

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode([WIDTH,HEIGHT])
pg.display.set_caption("Simulation")
bg = sp.sprite('background.png', [0,0])
screen.blit(bg.image, bg.rect)

returningAnimals = []
objectsIndex = 1
objectsDictionary = {}
food = []
rabbits = []
wolfs = []
indexMap = [['g' for i in range (800)] for j in range (800)]
turn = 1
rabbitDens = [dn.den(100,100), dn.den(100, 700), dn.den(700, 100), dn.den(700, 700)]
wolfDens = [dn.den(400,400), dn.den(200,200), dn.den(600,600)]

#def createPerimeter(x,y,h):
#    perimeter = []

def markMap(object):
    global indexMap

    indexMap[object.rect.center[1]%800][object.rect.center[0]%800] = object.index

    indexMap[object.rect.top][object.rect.left] = object.index
    indexMap[object.rect.top][(object.rect.left+object.rect.h)%800] = object.index
    indexMap[(object.rect.top+object.rect.h)%800][(object.rect.left+object.rect.h)%800] = object.index
    indexMap[(object.rect.top+object.rect.h)%800][object.rect.left] = object.index
    #for i in range (object.rect.h):
    #    for j in range(object.rect.w):
    #        indexMap[(object.rect.top + i) % 800][(object.rect.left + j) % 800] = object.index

def clearMap(x,y,x2,y2,h):
    global indexMap
    
    indexMap[y2%800][x2%800] = 'g'

    indexMap[y][x] = 'g'
    indexMap[y][(x + h)%800] = 'g'
    indexMap[(y+h)%800][(x + h)%800] = 'g'
    indexMap[(y+h)%800][x] = 'g'
    #for i in range (h):
    #    for j in range(h):
    #        indexMap[(y + i) % 800][(x + j) % 800] = 'g'

def drawScreen(surface):
    for carrot in food:
        surface.blit(carrot.image, carrot.rect)
    for rabbit in rabbits:
        surface.blit(rabbit.image, rabbit.rect)
    for wolf in wolfs:
        surface.blit(wolf.image, wolf.rect)

    pg.display.update()

def createFood(n):
    global objectsIndex, indexMap, objectsDictionary
    for i in range(n):
        cIndex = 'c'+ str(objectsIndex)
   
        carrot = crt.carrot(screen, cIndex, 1, WIDTH - 11, 1, HEIGHT - 11)
    
        food.append(carrot)
        objectsDictionary[carrot.index] =  carrot
        objectsIndex += 1
        markMap(carrot)

def createAnimals(nrabbits, nwolfs):
    global objectsIndex, indexMap, objectsDictionary
    for i in range(nrabbits):
        rIndex = 'r' + str(objectsIndex)
        startingDen = rnd.choice(rabbitDens)
        rabbit = rb.rabbit(screen, rIndex, startingDen.posx, startingDen.posy, RABBIT_MOVEMENT_SPEED, RABBIT_SENSE, startingDen)
        rabbits.append(rabbit)
        objectsDictionary[rabbit.index] = rabbit
        objectsIndex += 1
        markMap(rabbit)

    for i in range(nwolfs):
        wIndex = 'w' + str(objectsIndex)
        startingDen = rnd.choice(wolfDens)
        wolf = wlf.wolf(screen, wIndex, startingDen.posx, startingDen.posy, WOLF_MOVEMENT_SPEED, WOLF_SENSE, startingDen)
        wolfs.append(wolf)
        objectsDictionary[wolf.index] = wolf
        objectsIndex += 1


#print(objectsDictionary)
createFood(1800)
createAnimals(8, 3)

###NIGHT
#def animalBehavior(animals, target):

#    for animal in animals:
#        ###to change
#        if animal.energy <= 0:
#            animal.dead = True
#            animals.remove(animal)
#        elif animal.energy > animal.reproduction*animal.maxEnergy:
#            if animals == rabbits:
#                newAnimal = rb.rabbit
#            elif animals == wolfs:
#                newAnimal = wlf.wolf
#            animal.reproduce(animals, newAnimal, objectsIndex, objectsDictionary)

def animalBehavior(animal, targets):

    animal.move(bg.image, indexMap, objectsDictionary)

    eat = animal.selfScan(indexMap)
    if eat[0] == animal.prey:

        target = objectsDictionary.get(eat)
        if target.dead != True:
            animal.eaten.append(target.rect.center)
            clearMap(target.rect.left,target.rect.top,target.rect.center[0], target.rect.center[1], target.rect.h)
            screen.blit(bg.image, target.rect, target.rect)
            objectsDictionary.pop(eat)
            target.dead = True
            animal.energy = (animal.energy + target.energyRep) % animal.maxEnergy
            targets.remove(target)
            animal.wandering = True

def day():
    global objectsIndex, indexMap, objectsDictionary

    for carrot in food:
        markMap(carrot)
    
    for rabbit in rabbits:
              

        animalBehavior(rabbit, food)

        clearMap(rabbit.oldPosition[0],rabbit.oldPosition[1], rabbit.oldCenter[0], rabbit.oldCenter[1], rabbit.rect.h)
        markMap(rabbit)

        #multithreading!!!
    for wolf in wolfs:
            
        animalBehavior(wolf, rabbits)

    drawScreen(screen)


def night_d():
    for animal in list(returningAnimals):
        animal.moveBackToDen(bg.image)
        if animal.getPosition() == animal.den.getPosition():
            returningAnimals.remove(animal)
    drawScreen(screen)

def night_s():
    global rabbits, wolfs, objectsIndex, indexMap, objectsDictionary, rabbitDens, returningAnimals

    print ('night')

    for rabbit in list(rabbits):



        if rabbit.energy > rabbit.reproduciton*rabbit.maxEnergy:
            #rabbit.backToDen(bg.image ,rabbit.den[0], rabbit.den[1])
            rabbit.findClosestDen(rabbitDens)

            clearMap(rabbit.rect.left,rabbit.rect.top, rabbit.rect.center[0], rabbit.rect.center[1], rabbit.rect.h)

            #########
            #markMap(rabbit)
            
            rabbit.reproduce(rabbits, rb.rabbit, objectsIndex, objectsDictionary)
            objectsIndex += 1 
            returningAnimals.append(rabbit)

        elif rabbit.energy <= 0:
            clearMap(rabbit.rect.left, rabbit.rect.top, rabbit.rect.center[0], rabbit.rect.center[1], rabbit.rect.h)
            rabbit.dead = True
            rabbits.remove(rabbit)
            objectsDictionary.pop(rabbit.index)
            rabbit.surface.blit(bg.image, (rabbit.getPosition()))

        else:
            #rabbit.backToDen(bg.image ,rabbit.den[0], rabbit.den[1])
            rabbit.findClosestDen(rabbitDens)
            clearMap(rabbit.oldPosition[0],rabbit.oldPosition[1], rabbit.oldCenter[0], rabbit.oldCenter[1], rabbit.rect.h)
            #markMap(rabbit)
            returningAnimals.append(rabbit)
    
    for wolf in list(wolfs):

        if wolf.energy > wolf.reproduciton*wolf.maxEnergy:
            #wolf.backToDen(bg.image ,wolf.den[0], wolf.den[1])
            wolf.findClosestDen(wolfDens)
            wolf.reproduce(wolfs, wlf.wolf, objectsIndex, objectsDictionary)
            objectsIndex += 1
            returningAnimals.append(wolf)
        elif wolf.energy <= 0:
            wolf.dead = True
            wolfs.remove(wolf)
            objectsDictionary.pop(wolf.index)
            wolf.surface.blit(bg.image, (wolf.getPosition()))
        
        else:
            wolf.findClosestDen(wolfDens)
            returningAnimals.append(wolf)

    createFood(500)
    drawScreen(screen)



def main():
    global turn, objectsIndex, indexMap, objectsDictionary, returningAnimals
    running = True

    while running:
        
        clock.tick(SPEED)

        while turn < 100:
            clock.tick(SPEED)
            day()
            turn += 1
            print (turn)
        
        night_s()
        while len(returningAnimals) > 0:
            clock.tick(SPEED)
            night_d()

        turn = 1
        #if turn == 50:
        #    screen.blit(bg.image , food[1].rect, food[1].rect)
        #    food.pop(1)
        #if turn == 400:
        #    pg.quit()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit("quit")
           

main()