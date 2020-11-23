import pygame as pg
import sprites as sp
import carrot as crt
import rabbit as rb
import sys
import colours

WIDTH = 500
HEIGHT = 500
SPEED = 20

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
indexMap = [[-1 for i in range (500)] for j in range (500)]
turn = 1

def markMap(object):
    global indexMap

    for i in range (object.rect.h):
        for j in range(object.rect.w):
            indexMap[(object.rect.left + j) % 500][(object.rect.top + i) % 500] = object.index

def drawScreen(surface):

    for carrot in food:
        surface.blit(carrot.image, carrot.rect)
    for rabbit in rabbits:
        surface.blit(rabbit.image, rabbit.rect)

    pg.display.update()

for i in range(60):
    carrot = crt.carrot(screen, objectsIndex, 1, WIDTH - 11, 1, HEIGHT - 11)
    food.append(carrot)
    objectsDictionary[carrot.index] =  carrot
    objectsIndex += 1
    markMap(carrot)

for i in range(1):
    rabbit = rb.rabbit(screen, objectsIndex, 250, 250, 10, 30)
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
            rabbit.move(bg.image, indexMap, objectsDictionary)

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