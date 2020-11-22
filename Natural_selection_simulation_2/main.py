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

objectIndex = 10
food = [crt.carrot(screen, 1, WIDTH - 11, 1, HEIGHT - 11) for i in range (2)]
rabbits = [rb.rabbit(screen, objectIndex, 250, 250, 10, 10) for i in range(50)]


turn = 1

def drawScreen(surface):

    for carrot in food:
        surface.blit(carrot.image, carrot.rect)
    for rabbit in rabbits:
        surface.blit(rabbit.image, rabbit.rect)

    pg.display.update()

def main():
    global turn, objectIndex
    running = True
    while running:
        
        clock.tick(SPEED)

        for rabbit in rabbits:
            rabbit.move(bg.image)

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