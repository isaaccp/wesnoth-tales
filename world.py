import yaml
import pygame
from area import Area
from display import Display

class World:
    def __init__(self, world):
        self.old_area = None
        self.area = None
        self.areas = None
        self.world_map = None
        self.load_world(world)
        self.display = Display(self)
        self.cursor = pygame.image.load('images/cursors/normal.png')

    def load_world(self, name):
        f = open('data/world/%s' % name)
        data = yaml.load(f)
        f.close()
        self.world_map = pygame.image.load('images/maps/%s.png' % data['image'])
        self.area = Area(data['start_area'])
        self.areas = data['areas']

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

    def draw(self, screen):
        if self.area:
            self.display.draw(screen)
        else:
            screen.blit(self.world_map, (0,0))
            for a in self.areas:
                pygame.draw.rect(screen, (255, 0, 0),
                    pygame.Rect(a['pos'], a['size']), 2)
            mouse = pygame.mouse.get_pos()
            r = mouse
            screen.blit(self.cursor, r)





    def process_event(self, event):
        self.display.process_event(event)
