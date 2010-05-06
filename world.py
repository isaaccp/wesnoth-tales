import pygame
from area import Area
from display import Display
from character import Character

class World:
    def __init__(self):
        self.area = Area('hill.area')
        self.display = Display(self)
        self.characters = []
        ranger = Character('ranger')
        ranger.set_location(6,0)
        self.characters.append(ranger)

    def update(self, proportion):
        #update things in world

        #update display (i.e., scroll)
        self.display.update(proportion)

    def draw(self, screen):
        self.display.draw(screen)

    def process_event(self, event):
        self.display.process_event(event)
