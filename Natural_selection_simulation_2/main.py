import pygame as pg
import sprites as sp
import sys
import colours

WIDTH = 500
HEIGHT = 500
SPEED = 20

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode([WIDTH,HEIGHT])
pg.display.set_caption("Simulation")
bg = sp.Background('background.png', [0,0])

def drawScreen(surface):
    surface.blit(bg.image, bg.rect)

    pg.display.update()

def main():
    running = True
    while running:
        
        clock.tick(SPEED)

        drawScreen(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit("quit")
           

main()