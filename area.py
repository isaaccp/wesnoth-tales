import yaml
import pygame
from random import randint, choice
from numpy import array, empty
from constants import *
from character import Character
from location import Location
import a_star

class Area:
    def __init__(self, world, area, gate=1):
        self.tiles = {}
        self.area = area
        self.map = None
        self.gates = {}

        self.transition = None
        self.characters = []

        # hash to cache paths
        self.paths = {}

        self.load(world, area)

    def recalculate_free_locations(self):
        self.free_locations = {}
        for i in range(self.w):
            for j in range(self.h):
                loc = Location(i, j)
                if self.can_pass(None, loc):
                    self.free_locations[loc] = True
        return True

    def place_hero_in_gate(self, hero, gate):
        self.place_character(hero, self.gates[gate]['tiles'][0], is_hero=True)

    def remove_hero(self):
        hero = self.characters.pop(0)
        loc = hero.location()
        self.map[loc.x][loc.y]['character'] = None
        self.free_locations[l] = True

    def is_character_hero(self, character):
        return character == self.characters[0]

    def place_character(self, character, loc, is_hero=False):
        """Places a character in the map for the first time"""
        #FIXME: check for already existing characters
        character.set_location(loc)
        if is_hero:
            self.characters.insert(0, character)
        else:
            self.characters.append(character)
        self.map[loc.x][loc.y]['character'] = character
        del self.free_locations[loc]

    def move_character(self, character, loc, moves_left):
        """Moves the character in the map"""
        #FIXME: check for already existing characters
        del self.map[character.loc.x][character.loc.y]['character']
        self.free_locations[character.loc] = True
        character.set_location(loc)
        self.map[loc.x][loc.y]['character'] = character
        del self.free_locations[character.loc]
        self.invalidate_paths()
        if self.is_character_hero(character):
            gate = self.has_gate(loc)
            if gate and not moves_left:
                self.transition = self.gates[gate]

    def invalidate_paths(self):
        self.paths = {}

    def load(self, world, area):
        f = open('data/worlds/%s/%s' % (world, area))
        data = yaml.load(f) 
        f.close()
        for i in data['import']:
            self.load_import(world, i)
        self.load_map(world, data['map']) 
        # FIXME: probably this will be removed when we take into account units
        # that can be in water or blocking areas
        self.recalculate_free_locations()
        for g in data['gates']:
            gate = int(g['id'])
            dest = g['dest']
            self.gates[gate]['next'] = dest
        for u in data['units']:
            if u['type'] == 'unique':
                pass
            elif u['type'] == 'fill':
                # FIXME: should probably be non-blocking grids instead of just
                # w*h
                units = (self.w * self.h) / u['density']
                unit_types = u['unit_types']
                sum_prob = sum([ut['prob'] for ut in unit_types])
                for i in range(units):
                    rnd = randint(0, sum_prob - 1)
                    s = 0
                    for ut in unit_types:
                        s = s + ut['prob']
                        if rnd < s:    
                            c = Character.load_from_data(ut['data'])
                            self.place_character(c, self.random_free_location(c))
                            break

    def load_import(self, world, name):
        f = open('data/worlds/%s/%s' % (world, name))
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
        s = 0
        for img in image_list:
            s = s + img['prob']
            if rnd < s:
                return img['image']

    def load_map(self, world, name):
        f = open('data/worlds/%s/%s' % (world, name))
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
        self.w, self.h = self.map.shape

    def random_free_location(self, unit):
        loc = choice(self.free_locations.keys())
        return loc

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
        # FIXME: for now we don't use unit, go over uses of can_pass if 
        # we actually start requiring it
        if self.map[loc.x][loc.y]['tile']['type'] != 'normal':
            return False
        if self.map[loc.x][loc.y].has_key('character'):
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
