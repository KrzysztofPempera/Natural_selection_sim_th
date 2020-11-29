import pygame as pg
import sprites as sp
import carrot as crt
import rabbit as rb
import sys
import colours
import json

with open('para.json', 'r') as para:
    config = json.load(para)

WIDTH = 500
HEIGHT = 500
SPEED = 2
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
indexMap = [['g' for i in range (500)] for j in range (500)]
turn = 1

def markMap(object):
    global indexMap
    for i in range (object.rect.h):
        for j in range(object.rect.w):
            indexMap[(object.rect.top + i) % 500][(object.rect.left + j) % 500] = object.index

def clearMap(x,y,h):
    global indexMap
    for i in range (h):
        for j in range(h):
            indexMap[(y + i) % 500][(x + j) % 500] = 'g'

def drawScreen(surface):
    for carrot in food:
        surface.blit(carrot.image, carrot.rect)
    for rabbit in rabbits:
        surface.blit(rabbit.image, rabbit.rect)

    pg.display.update()

for i in range(100):
    cIndex = 'c'+ str(objectsIndex)
    carrot = crt.carrot(screen, cIndex, 1, WIDTH - 11, 1, HEIGHT - 11)
    food.append(carrot)
    objectsDictionary[carrot.index] =  carrot
    objectsIndex += 1
    markMap(carrot)
     
for i in range(2):
    rIndex = 'r' + str(objectsIndex)
    rabbit = rb.rabbit(screen, rIndex, 250, 250, RABBIT_MOVEMENT_SPEED, RABBIT_SENSE)
    rabbits.append(rabbit)
    objectsDictionary[rabbit.index] = rabbit
    objectsIndex += 1
    markMap(rabbit)

def main():
    global turn, objectIndex, indexMap, objectsDictionary
    running = True
    while running:
        
        clock.tick(SPEED)

        for rabbit in rabbits:
            
            if rabbit.energy <= 0:
                rabbit.dead = True
                rabbits.remove(rabbit)
            rabbit.move(bg.image, indexMap, objectsDictionary)
            clearMap(rabbit.oldPosition[0],rabbit.oldPosition[1],rabbit.rect.h)
            eat = rabbit.selfScan(indexMap)

            if eat != 'g':
                target = objectsDictionary.get(eat)
                if target.dead != True:
                    clearMap(target.rect.left,target.rect.top,target.rect.h)
                    screen.blit(bg.image, target.rect, target.rect)
                    objectsDictionary.pop(eat)
                    target.dead = True
                    rabbit.energy += (target.energyRep) % rabbit.maxEnergy
                    food.remove(target)
                    rabbit.wandering = True

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