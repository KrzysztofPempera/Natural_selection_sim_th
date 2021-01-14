import pygame as pg
import json

with open('para.json', 'r') as para:
    config = json.load(para)

class den(object):

    def __init__(self, posx, posy):

        self.posx = posx
        self.posy = posy
        
        self.animals = []

    def getPosition(self):
        return self.posx, self.posy