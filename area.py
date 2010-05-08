import yaml
import pygame
from random import randint
from numpy import array, empty
from constants import *
from character import Character
from location import Location
import a_star

class Area:
    def __init__(self, area, gate=1):
        self.tiles = {}
        self.area = area
        self.map = None
        self.gates = {}

        self.transition = None
        self.characters = []

        # hash to cache paths
        self.paths = {}

        self.load(area)
        self.w, self.h = self.map.shape

    def place_hero_in_gate(self, gate):
        ranger = Character('ranger')
        self.place_character(ranger, self.gates[gate]['tiles'][0])

    def remove_hero(self):
        hero = self.characters.pop(0)
        loc = hero.location()
        self.map[loc.x][loc.y]['character'] = None

    def place_character(self, character, loc):
        """Places a character in the map for the first time"""
        #FIXME: check for already existing characters
        character.set_location(loc)
        self.characters.append(character)
        self.map[loc.x][loc.y]['character'] = character

    def move_character(self, character, loc, moves_left):
        """Moves the character in the map"""
        #FIXME: check for already existing characters
        del self.map[character.loc.x][character.loc.y]['character']
        character.set_location(loc)
        self.map[loc.x][loc.y]['character'] = character
        self.invalidate_paths()
        gate = self.has_gate(loc)
        if gate and not moves_left:
            self.transition = self.gates[gate]

    def invalidate_paths(self):
        self.paths = {}

    def load(self, area):
        f = open('data/world/%s' % area)
        lines = f.readlines()
        for l in lines:
            parts = l.rstrip().split(' ')
            if parts[0] == 'import':
                self.load_yaml(parts[1])
            elif parts[0] == 'map':
                self.load_map(parts[1])
            elif parts[0] == 'gate':
                gate = int(parts[1])
                next_area = parts[2]
                if next_area == 'world':
                    next_gate = self.area
                else:
                    next_gate = int(parts[3])
                self.gates[gate]['next'] = {
                    'area': next_area,
                    'gate': next_gate
                }

    def load_yaml(self, yaml_file):
        f = open('data/world/%s' % yaml_file)
        data = yaml.load(f) 
        f.close()
        for t in data['tiles']:
            prob_sum = 0
            for i in t['flat']:
                i['image'] = pygame.image.load('images/%s.png' % i['file'])
                prob_sum = prob_sum + i['prob']
            t['flat_prob_sum'] = prob_sum

            prob_sum = 0
            if t.has_key('volume'):
                for i in t['volume']:
                    i['image'] = pygame.image.load('images/%s.png' % i['file'])
                    prob_sum = prob_sum + i['prob']
                t['volume_prob_sum'] = prob_sum
            self.tiles[t['char']] = t

    def select_image(self, image_list, prob_max):
        rnd = randint(0, prob_max - 1) 
        sum = 0
        for img in image_list:
            sum = sum + img['prob']
            if rnd < sum:
                return img['image']

    def load_map(self, map_file):
        f = open('data/world/%s' % map_file)
        lines = [l.rstrip("\n") for l in f.readlines()]
        f.close()

        y = len(lines)
        x = len(lines[0])/2
        self.map = empty((x,y), dtype=object)
        for j in range(y):
            for i in range(x):
                c = lines[j][i*2]
                extra = lines[j][i*2+1]
                t = self.tiles[c]
                self.map[i][j] = {
                    'char': c,
                    'tile': t
                }
                if extra != ' ':
                    if extra.isdigit():
                        gate = int(extra)
                        self.map[i][j]['gate'] = gate
                        if not self.gates.has_key(gate):
                            self.gates[gate] = {}
                        if not self.gates[gate].has_key('tiles'):
                            self.gates[gate]['tiles'] = []
                        self.gates[gate]['tiles'].append(Location(i,j))

                self.map[i][j]['flat_image'] = self.select_image(t['flat'],
                    t['flat_prob_sum'])
                if t.has_key('volume'):
                    self.map[i][j]['volume_image'] = \
                        self.select_image(t['volume'], t['volume_prob_sum'])

    def can_move(self, unit, loc): 
        #FIXME: probably we want to remove this trivial check from here
        # by ensuring this method is always called on a proper loc
        if loc.x < 0 or loc.x >= self.w:
            return False
        if loc.y < 0 or loc.y >= self.h:
            return False
        if self.map[loc.x][loc.y]['tile']['type'] != 'normal':
            return False
        if self.map[loc.x][loc.y].has_key('character'):
            return False
        path = self.find_path(unit, loc)
        if not path:
            return False
        return path

    def can_pass(self, unit, loc): 
        if self.map[loc.x][loc.y]['tile']['type'] != 'normal':
            return False
        return True

    def has_gate(self, loc):
        if self.map[loc.x][loc.y].has_key('gate'):
            return self.map[loc.x][loc.y]['gate']
        else:
            return False

    def find_path(self, unit, loc):
        #FIXME: remember to invalidate paths
        path_id = (unit, loc)
        if not self.paths.has_key(path_id):
            self.paths[path_id] = a_star.find_path(self, unit, loc)

        return self.paths[path_id]

    def update(self, proportion):
        for c in self.characters:
            c.update(self, proportion)
