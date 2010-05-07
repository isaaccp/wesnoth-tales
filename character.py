import pygame
from location import Location

class Character:
    def __init__(self, name):
        self.name = name
        self.image = pygame.image.load('images/units/%s.png' % name)

        self.loc = None
        self.dest = None
        self.path = None
        self.completion = None
        self.action = None

    def location(self):
        return self.loc

    def set_location(self, loc):
        self.loc = loc

    def move(self, path):
        self.path = path[1:]
        self.completion = 0
        self.action = 'move'

    def update(self, area, proportion):
        if self.action == 'move':
            #FIXME: check if the path is still free and that kind of things
            if self.path and not self.dest:
                self.dest = self.path.pop(0)
                if len(self.path) == 0:
                    self.path = None
            self.completion = self.completion + proportion * 50
            if self.completion > 100:
                area.move_character(self, self.dest, self.path)
                self.dest = None
                self.completion = 0
                if not self.path:
                    self.action = None
