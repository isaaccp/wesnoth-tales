import pygame
from area import Area
from display import Display

class World:
    def __init__(self):
        self.area = Area('hill.area')
        self.display = Display(self)

    def update(self, proportion):
        #update things in world

        #update display (i.e., scroll)
        self.display.update(proportion)

    def draw(self, screen):
        self.display.draw(screen)

    def process_event(self, event):
        self.display.process_event(event)
