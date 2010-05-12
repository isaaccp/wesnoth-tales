import yaml
import pygame
from constants import *
from location import Location

class Character:
    def __init__(self):
        self.loc = None
        self.dest = None
        self.path = None
        self.completion = None
        self.action = None

    @staticmethod
    def load_from_file(path, name):
        f = open('%s/%s.yaml' % (path, name))
        data = yaml.load(f)
        f.close()

        return Character.load_from_data(data)

    @staticmethod
    def load_from_data(data):
        char = Character()
        if data.has_key('unit'):
            #FIXME: load unit from file and be done with it
            pass
        else:
            char.char_class = data['class']
            char.race = data['race']
            # FIXME: probably pass area info too and have a general level for
            # creatures roaming the area instead of defaulting to one
            if data.has_key('level'):
                char.level = data['level']
            else:
                char.level = 1
            char.image = pygame.image.load('images/units/%s.png' % data['class'])
        return char

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
