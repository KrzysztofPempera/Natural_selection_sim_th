import pygame as pg
import random as rnd
import numpy as np
import math

class animal(object):
    
    def __init__(self, surface, index, movementspeed, sense):
        self.surface = surface
        self.index = index
        self.sense = sense
        self.ms = movementspeed

        self.eat = False
        self.wandering = True
        self.velocity = (0 ,0)
        self.target = object
        self.oldPosition = (-1, -1)
        self.age = 0

        