import pygame
from area import Area
from display import Display

class World:
    def __init__(self):
        self.old_area = None
        self.area = Area('hill.area')
        self.display = Display(self)

    def update(self, proportion):
        #update things in world
        self.area.update(proportion)

        if self.area.transition:
            t = self.area.transition['next']
            if t['area'] == 'world':
                pass
            else:
                self.area = Area(t['area'], t['gate'])
       
        new_area = not self.old_area or (self.area != self.old_area)
        self.old_area = self.area

        #update display (i.e., scroll)
        self.display.update(proportion, new_area)

    def draw(self, screen):
        self.display.draw(screen)

    def process_event(self, event):
        self.display.process_event(event)
