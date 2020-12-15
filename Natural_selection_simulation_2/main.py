import pygame as pg
import sprites as sp
import carrot as crt
import rabbit as rb
import wolf as wlf
import sys
import colours
import json

with open('para.json', 'r') as para:
    config = json.load(para)

WIDTH = 800
HEIGHT = 800
SPEED = 24
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

objectsIndex = 1
objectsDictionary = {}
food = []
rabbits = []
wolfs = []
indexMap = [['g' for i in range (800)] for j in range (800)]
turn = 1

def markMap(object):
    global indexMap
    for i in range (object.rect.h):
        for j in range(object.rect.w):
            indexMap[(object.rect.top + i) % 800][(object.rect.left + j) % 800] = object.index

def clearMap(x,y,h):
    global indexMap
    for i in range (h):
        for j in range(h):
            indexMap[(y + i) % 800][(x + j) % 800] = 'g'

def drawScreen(surface):
    for carrot in food:
        surface.blit(carrot.image, carrot.rect)
    for rabbit in rabbits:
        surface.blit(rabbit.image, rabbit.rect)
    for wolf in wolfs:
        surface.blit(wolf.image, wolf.rect)

    pg.display.update()


for i in range(1800):
    cIndex = 'c'+ str(objectsIndex)
   

    carrot = crt.carrot(screen, cIndex, 1, WIDTH - 11, 1, HEIGHT - 11)
    
    food.append(carrot)
    objectsDictionary[carrot.index] =  carrot
    objectsIndex += 1
    markMap(carrot)
     
for i in range(200):
    rIndex = 'r' + str(objectsIndex)
    rabbit = rb.rabbit(screen, rIndex, 250, 250, RABBIT_MOVEMENT_SPEED, RABBIT_SENSE)
    rabbits.append(rabbit)
    objectsDictionary[rabbit.index] = rabbit
    objectsIndex += 1
    markMap(rabbit)

for i in range(0):
    wIndex = 'w' + str(objectsIndex)
    wolf = wlf.wolf(screen, wIndex, 200, 200, WOLF_MOVEMENT_SPEED, WOLF_SENSE)
    wolfs.append(wolf)
    objectsDictionary[wolf.index] = wolf
    objectsIndex += 1

def main():
    global turn, objectsIndex, indexMap, objectsDictionary
    running = True
    while running:
        
        clock.tick(SPEED)

        for rabbit in rabbits:
            
            if rabbit.energy <= 0:
                rabbit.dead = True
                rabbits.remove(rabbit)
            elif rabbit.energy > rabbit.reproduciton*rabbit.maxEnergy:
                rabbit.reproduce(rabbits, rb.rabbit, objectsIndex, objectsDictionary)
                objectsIndex += 1          

            rabbit.move(bg.image, indexMap, objectsDictionary)

            eat = rabbit.selfScan(indexMap)

            if eat[0] == rabbit.prey:
                target = objectsDictionary.get(eat)
                if target.dead != True:
                    clearMap(target.rect.left,target.rect.top,target.rect.h)
                    screen.blit(bg.image, target.rect, target.rect)
                    objectsDictionary.pop(eat)
                    target.dead = True
                    rabbit.energy += (target.energyRep) % rabbit.maxEnergy
                    food.remove(target)
                    rabbit.wandering = True

           
            clearMap(rabbit.oldPosition[0],rabbit.oldPosition[1],rabbit.rect.h)


            if rabbit.dead == True:
                objectsDictionary.pop(rabbit.index)
                pos = rabbit.getPosition()
                clearMap(pos[0], pos[1], rabbit.rect.h)
            else:
                markMap(rabbit)
        #multithreading!!!
        for wolf in wolfs:
            
            if wolf.energy <= 0:
                wolf.dead = True
                wolfs.remove(wolf)
            elif wolf.energy > wolf.reproduciton*wolf.maxEnergy:
                wolf.reproduce(wolfs, wlf.wolf, objectsIndex, objectsDictionary)
                objectsIndex += 1
           
            wolf.move(bg.image, indexMap, objectsDictionary)
            
            eat = wolf.selfScan(indexMap)

            if eat[0] == wolf.prey:
                target = objectsDictionary.get(eat)
                if target.dead != True:
                    clearMap(target.rect.left,target.rect.top,target.rect.h)
                    screen.blit(bg.image, target.rect, target.rect)
                    objectsDictionary.pop(eat)
                    target.dead = True
                    wolf.energy += (target.energyRep) % wolf.maxEnergy
                    rabbits.remove(target)
                    wolf.wandering = True            


            if wolf.dead == True:
                objectsDictionary.pop(wolf.index)

        drawScreen(screen)

        turn += 1
        #if turn == 50:
        #    screen.blit(bg.image , food[1].rect, food[1].rect)
        #    food.pop(1)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit("quit")
           

main()