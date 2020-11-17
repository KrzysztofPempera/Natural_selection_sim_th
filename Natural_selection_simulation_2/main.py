import pygame as pg
import sprites as sp
import carrot as crt
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

carrot = crt.carrot(screen, 1, WIDTH - 11, 1, HEIGHT - 11)
objectIndex = 10

turn = 1

def drawScreen(surface):
    surface.blit(bg.image, bg.rect)
    surface.blit(carrot.image, carrot.rect)
    pg.display.update()

def main():
    global turn, objectIndex
    running = True
    while running:
        
        clock.tick(SPEED)

        drawScreen(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit("quit")
           

main()