import yaml
import pygame
from area import Area
from display import Display

class World:
    def __init__(self, world):
        self.name = world
        self.main_areas = None
        self.areas = {}
        self.world_map = None
        self.load_world(world)
        self.cursor = pygame.image.load('images/cursors/normal.png')

    def get_start_area(self):
        return self.get_area(self.start_area)

    def get_area(self, area):
        if not self.areas.has_key(area):
            self.areas[area] = Area(self.name, area)
        return self.areas[area]

    def load_world(self, name):
        f = open('data/worlds/%s/world.yaml' % name)
        data = yaml.load(f)
        f.close()
        self.map = data['map']
        self.start_area = data['start_area']
        self.main_areas = data['areas']

    def update(self, proportion):
        if self.area:
            # update things in world
            self.area.update(proportion)

            if self.area.transition:
                t = self.area.transition['next']
                #FIXME: in the future areas will suffer changes and we'll have
                # to save the changes
                if t['area'] == 'world':
                    self.area = None
                else:
                    self.area = Area(t['area'], t['gate'])
            new_area = not self.old_area or (self.area != self.old_area)
            self.old_area = self.area

            if self.area:
                # update display (i.e., scroll)
                self.display.update(proportion, new_area)
