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
import csv
import os
from graph import plot

with open('para.json', 'r') as para:
    config = json.load(para)

with open ('ident.json', 'r') as jsonFile:
    indent = json.load(jsonFile)
    REPORT_ID = int(indent['id'])


WIDTH = 800
HEIGHT = 800
SPEED = 50
RABBIT_MOVEMENT_SPEED = config['RABBIT_MOVEMENT_SPEED']
WOLF_MOVEMENT_SPEED = config['WOLF_MOVEMENT_SPEED']
WOLF_SENSE = config['WOLF_SENSE']
RABBIT_SENSE = config['RABBIT_SENSE']
CARROT_REP = config['CARROT_REP']
RABBIT_THREAT = config['RABBIT_THREAT']

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode([WIDTH,HEIGHT])
pg.display.set_caption("Simulation")
bg = pg.image.load('backgroundForest.png')
screen.blit(bg,(0,0))

days = 0
wolfCount = []
rabbitCount = []
foodCount = []
rabbitMS = []
rabbitS = []
rabbitT = []
wolfMS = []
wolfS = []

returningAnimals = []
objectsIndex = 1
objectsDictionary = {}
food = []
rabbits = []
wolfs = []
pathMap = [[0 for i in range (800)] for j in range (800)]
traceMap = [[0 for i in range (800)] for j in range (800)]
indexMap = [['g' for i in range (800)] for j in range (800)]
terrainMap = [[0 for i in range (800)] for j in range (800)]
for i in range (350):
    for j in range(350):
        terrainMap[i][j] = 1

turn = 1
rabbitDens = [dn.den(100,390,'rabbitDen.png'), dn.den(100, 700,'rabbitDen.png'), dn.den(700, 100,'rabbitDen.png'), dn.den(700, 700,'rabbitDen.png')]
wolfDens = [dn.den(400,500, 'wolfDen.png'), dn.den(450,100, 'wolfDen.png'), dn.den(650,360, 'wolfDen.png')]

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
    surface.blit(bg,(0,0))

    for carrot in food:
        surface.blit(carrot.image, carrot.rect)
    for rabbit in rabbits:
        surface.blit(rabbit.image, rabbit.rect)
    for wolf in wolfs:
        surface.blit(wolf.image, wolf.rect)
    for den in list(rabbitDens+wolfDens):
        surface.blit(den.image, den.rect)
    pg.display.update()

def createFood(n):
    global objectsIndex, indexMap, objectsDictionary
    locations = {}
    locations['forest'] = [1,300,1,350]
    locations['plains1'] = [311,WIDTH-11,1,350]
    locations['plains2'] = [1,WIDTH-11, 350, HEIGHT-11]
    locationsKeys = ['forest','plains1','plains2']
    for i in range(n):
        cIndex = 'c'+ str(objectsIndex)
        location = rnd.choices(locationsKeys,weights= [1,5,7])
        location = locations[location[0]]
        carrot = crt.carrot(screen, cIndex, location[0], location[1], location[2], location[3])
    
        food.append(carrot)
        objectsDictionary[carrot.index] =  carrot
        objectsIndex += 1
        markMap(carrot)

def createAnimals(nrabbits, nwolfs):
    global objectsIndex, indexMap, objectsDictionary
    for i in range(nrabbits):
        rIndex = 'r' + str(objectsIndex)
        startingDen = rnd.choice(rabbitDens)
        rabbit = rb.rabbit(screen, rIndex, startingDen.posx, startingDen.posy, RABBIT_MOVEMENT_SPEED, RABBIT_SENSE, startingDen, RABBIT_THREAT)
        rabbits.append(rabbit)
        objectsDictionary[rabbit.index] = rabbit
        objectsIndex += 1

    for i in range(nwolfs):
        wIndex = 'w' + str(objectsIndex)
        startingDen = rnd.choice(wolfDens)
        wolf = wlf.wolf(screen, wIndex, startingDen.posx, startingDen.posy, WOLF_MOVEMENT_SPEED, WOLF_SENSE, startingDen)
        wolfs.append(wolf)
        objectsDictionary[wolf.index] = wolf
        objectsIndex += 1


#print(objectsDictionary)
createFood(1800)
createAnimals(60, 10)

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
    if animal.hidden == False:
        animal.move(indexMap, objectsDictionary, wolfDens, rabbitDens, pathMap)
        animal.leaveTrace(traceMap)
        eat = animal.selfScan(indexMap, terrainMap)
        if eat[0] == animal.prey:

            target = objectsDictionary.get(eat)
            if target.dead != True:
                animal.eaten.append(target.rect.center)
                clearMap(target.rect.left,target.rect.top,target.rect.center[0], target.rect.center[1], target.rect.h)
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


def night_3():
    global traceMap
    for den in rabbitDens:
        den.shareKnowledge(traceMap, pathMap)
        den.clearDen()
    for den in wolfDens:
        den.shareKnowledge(traceMap, pathMap)
        den.clearDen()
    traceMap = [[0 for i in range (800)] for j in range (800)]

def night_2():
    for animal in list(returningAnimals):
        animal.debuff = 1
        animal.moveBackToDen()
        if animal.getPosition() == animal.den.getPosition():
            returningAnimals.remove(animal)
    drawScreen(screen)

def night_1():
    global rabbits, wolfs, objectsIndex, indexMap, objectsDictionary, rabbitDens, returningAnimals

    print ('night')

    for rabbit in list(rabbits):


        rabbit.hidden = False
        #rabbit.wandering = True
        if rabbit.energy > rabbit.reproduciton*rabbit.maxEnergy:
            #rabbit.backToDen(bg.image ,rabbit.den[0], rabbit.den[1])
            rabbit.findClosestDen(rabbitDens)
            rabbit.den.animals.append(rabbit)
            clearMap(rabbit.oldPosition[0],rabbit.oldPosition[1], rabbit.oldCenter[0], rabbit.oldCenter[1], rabbit.rect.h)
            clearMap(rabbit.rect.left,rabbit.rect.top, rabbit.rect.center[0], rabbit.rect.center[1], rabbit.rect.h)

            #########
            #markMap(rabbit)
            
            rabbit.reproduce(rabbits, rb.rabbit, objectsIndex, objectsDictionary, rabbit.den.animals)
            objectsIndex += 1 
            returningAnimals.append(rabbit)

        elif rabbit.energy <= 0:
            clearMap(rabbit.oldPosition[0],rabbit.oldPosition[1], rabbit.oldCenter[0], rabbit.oldCenter[1], rabbit.rect.h)
            clearMap(rabbit.rect.left, rabbit.rect.top, rabbit.rect.center[0], rabbit.rect.center[1], rabbit.rect.h)
            rabbit.dead = True
            rabbits.remove(rabbit)
            objectsDictionary.pop(rabbit.index)

        else:
            #rabbit.backToDen(bg.image ,rabbit.den[0], rabbit.den[1])
            rabbit.findClosestDen(rabbitDens)
            rabbit.den.animals.append(rabbit)
            clearMap(rabbit.oldPosition[0],rabbit.oldPosition[1], rabbit.oldCenter[0], rabbit.oldCenter[1], rabbit.rect.h)
            clearMap(rabbit.rect.left,rabbit.rect.top, rabbit.rect.center[0], rabbit.rect.center[1], rabbit.rect.h)
            #markMap(rabbit)
            returningAnimals.append(rabbit)
    
    for wolf in list(wolfs):
       
        if wolf.energy > wolf.reproduciton*wolf.maxEnergy:
            #wolf.backToDen(bg.image ,wolf.den[0], wolf.den[1])
            wolf.findClosestDen(wolfDens)
            wolf.den.animals.append(wolf)
            wolf.reproduce(wolfs, wlf.wolf, objectsIndex, objectsDictionary, wolf.den.animals)
            objectsIndex += 1
            returningAnimals.append(wolf)
        elif wolf.energy <= 0:
            wolf.dead = True
            wolfs.remove(wolf)
            objectsDictionary.pop(wolf.index)
        
        else:
            wolf.findClosestDen(wolfDens)
            wolf.den.animals.append(wolf)
            returningAnimals.append(wolf)

    createFood(200)
    drawScreen(screen)


def report(day, wolfCount, rabbitCount, foodCount, rMS, rS, rT, wMS, wS):
    with open('report.csv', 'a', newline='') as csvfile:
        label = ['DAY','WOLF_COUNT','RABBIT_COUNT','FOOD_COUNT', 'RABBIT_MOVEMENT_SPEED', 'RABBIT_SENSE','RABBIT_THREAT', 'WOLF_MOVEMENT_SPEED', 'WOLF_SENSE']
        theWriter = csv.DictWriter(csvfile, fieldnames=label)
        theWriter.writerow({'DAY':day,'WOLF_COUNT':wolfCount, 'RABBIT_COUNT':rabbitCount, 'FOOD_COUNT':foodCount, 'RABBIT_MOVEMENT_SPEED':rMS, 'RABBIT_SENSE':rS, 'RABBIT_THREAT':rT,'WOLF_MOVEMENT_SPEED':wMS, 'WOLF_SENSE':wS})

def night_0():
    global rabbits, days, wolfs, wolfCount, rabbitCount, foodCount, rabbitMS, rabbitS, rabbitT, wolfMS, wolfS

    rabbitC = len(rabbits)
    wolfC = len(wolfs)
    foodC = len(food)
    wMS = 0
    wS = 0

    temp = 0
    if rabbits:
        for rabbit in rabbits:
            temp += rabbit.ms
        rMS = int(temp/len(rabbits))  

    temp = 0
    if rabbits:
        for rabbit in rabbits:
            temp += rabbit.sense
        rS = int(temp/len(rabbits))

    temp = 0
    if rabbits:
        for rabbit in rabbits:
            temp += rabbit.threatSense
        rT = int(temp/len(rabbits))

    temp = 0
    if wolfs:
        for wolf in wolfs:
            temp += wolf.ms
        wMS = int(temp/len(wolfs))

    temp = 0
    if wolfs:
        for wolf in wolfs:
            temp += wolf.sense
        wS = int(temp/len(wolfs))

    report(days, wolfC, rabbitC, foodC, rMS, rS, rT, wMS, wS)

    wolfCount.append(wolfC)
    rabbitCount.append(rabbitC)
    foodCount.append(foodC)
    rabbitMS.append(rMS)
    rabbitS.append(rS)
    rabbitT.append(rT)
    wolfMS.append(wMS)
    wolfS.append(wS)

def main():
    global turn, days, objectsIndex, indexMap, objectsDictionary, returningAnimals, wolfCount, rabbitCount, foodCount, rabbitMS, rabbitS, rabbitT, wolfMS, wolfS, REPORT_ID, indent
    running = True

    while running:
        
        clock.tick(SPEED)

        while turn < 150:
            clock.tick(SPEED)
            day()
            turn += 1
            print (turn)

        days += 1 
        night_0()
        night_1()
        while len(returningAnimals) > 0:
            clock.tick(SPEED)
            night_2()
        night_3()

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
        if days == 2:
            running = False
            pg.quit()
            plot(wolfCount, rabbitCount, rabbitMS, rabbitS, rabbitT, wolfMS, wolfS, REPORT_ID)
            indent['id'] = REPORT_ID + 1
            with open ('ident.json', 'w') as jsonFile:
                json.dump(indent, jsonFile)
            report_name = 'report_' + str(REPORT_ID) + '.csv'
            os.rename('report.csv', report_name)

main()