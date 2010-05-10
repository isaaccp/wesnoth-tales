import yaml
import pygame
from constants import *
from location import Location

class Character:
    def __init__(self, path, name):
        self.name = name
        self.load_character(path, name)

        self.loc = None
        self.dest = None
        self.path = None
        self.completion = None
        self.action = None

    def load_character(self, path, name):
        f = open('%s/%s.yaml' % (path, name))
        data = yaml.load(f)
        f.close()

        self.char_class = data['class']
        self.level = data['level']
        self.image = pygame.image.load('images/units/%s.png' % data['image'])

    def location(self):
        return self.loc

    def set_location(self, loc):
        self.loc = loc

    def move(self, path):
        self.path = path[1:]
        self.completion = 0
        self.action = 'move'

    def update(self, area, proportion):
        factor = proportion * step
        if self.action == 'move':
            # FIXME: check if the path is still free and that kind of things
            if self.path and not self.dest:
                self.dest = self.path.pop(0)
                if len(self.path) == 0:
                    self.path = None
            self.completion = self.completion + factor * 5
            # FIXME: it would be cool to move the completion over 100 go to the
            # next movement
            if self.completion > 100:
                area.move_character(self, self.dest, self.path)
                self.dest = None
                self.completion = 0
                if not self.path:
                    self.action = None
