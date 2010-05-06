import pygame
from area import Location
from constants import *

class Display:
    layers = ('TERRAIN', 'UNIT')

    def __init__(self, world):
        self.world = world
        self.map_area = pygame.Rect(0, 0, 640, 640)
        self.zoom = tile_size
        self.x_pos = 0
        self.y_pos = 0
        self.select = pygame.image.load('images/terrain/select.png')
        self.grid = pygame.image.load('images/terrain/grid.png')

    def hex_width(self):
        return (self.zoom*3)/4

    def hex_size(self):
        return self.zoom

    def pixel_position_to_hex(self, pos):
        x, y = pos
        x = x + self.x_pos
        y = y + self.y_pos
        s = self.hex_size()
        tess_x_size = self.hex_width() * 2
        tess_y_size = s
        x_base = (x / tess_x_size) * 2
        x_mod = x % tess_x_size
        y_base = y / tess_y_size
        y_mod = y % tess_y_size

        x_modifier, y_modifier = 0, 0

        if y_mod < (tess_y_size/2):
            if (x_mod * 2 + y_mod) < (s / 2):
                x_modifier, y_modifier = -1, -1
            elif (x_mod * 2 - y_mod) < ((s * 3) / 2):
                x_modifier, y_modifier = 0, 0
            else:
                x_modifier, y_modifier = 1, -1
        else:
            if x_mod * 2 - (y_mod - s / 2) < 0:
                x_modifier, y_modifier = -1, 0
            elif (x_mod * 2 + (y_mod - s / 2)) < s * 2:
                x_modifier, y_modifier = 0, 0
            else:
                x_modifier, y_modifier = 1, 0
        
        return Location(x_base + x_modifier, y_base + y_modifier)

    def get_location_x(self, loc): 
        return self.map_area.x + loc.x * self.hex_width() - self.x_pos

    def get_location_y(self, loc):
        y = self.map_area.y + loc.y * self.zoom - self.y_pos
        if (loc.x % 2) == 1:
            return y + self.zoom/2
        else:
            return y

    def rect(self, image, loc):
        x = self.get_location_x(loc) + self.hex_width()/2 - image.get_width()/2
        y = self.get_location_y(loc) + self.hex_size()/2 - image.get_height()/2
        return (x,y)

    def draw(self, screen):
        loc1 = self.pixel_position_to_hex((0,0))
        loc2 = self.pixel_position_to_hex((self.map_area.w, self.map_area.h))
        font = pygame.font.SysFont("Courier New",14)
        clip_rect = screen.set_clip(self.map_area)
        area = self.world.area
        for l in ['flat', 'volume', 'debug']:
            cur_layer = '%s_image' % l
            for i in range(loc1.x, loc2.x + 1):
                for j in range(loc1.y, loc2.y + 1):
                    loc = Location(i, j)
                    r = self.rect(self.grid, loc)
                    try:
                        t = area.map[i][j]
                    except Exception as inst:
                        break
                    if t.has_key(cur_layer):
                        r = self.rect(t[cur_layer], loc)
                        screen.blit(t[cur_layer], r)
                    elif l == 'debug':
                        if grid_enabled:
                            r = self.rect(self.grid, loc)
                            screen.blit(self.grid, r)
                        if coords_enabled:
                            text = font.render('(%d,%d)' % (i,j),1,(0,0,0))
                            r = self.rect(text, loc)
                            screen.blit(text, r)

        for c in self.world.characters:
            loc = Location(c.x, c.y)
            r = self.rect(c.image, loc)
            screen.blit(c.image, r)
            
        mouse = pygame.mouse.get_pos()
        loc = self.pixel_position_to_hex(mouse)
        r = self.rect(self.select, loc)
        screen.blit(self.select, r)
                        
        screen.set_clip(clip_rect)

    def update(self, proportion):
        mouse = pygame.mouse.get_pos()
        scroll = int(scroll_step * proportion)
        if mouse[0] < scroll_area_size:
            self.x_pos = self.x_pos - scroll
            if self.x_pos < 0:
                self.x_pos = 0
        elif mouse[0] > screen_width - scroll_area_size: 
            self.x_pos = self.x_pos + scroll
            if self.x_pos > (self.world.area.w * self.hex_width()) - self.map_area.w:
                self.x_pos = (self.world.area.w * self.hex_width()) - self.map_area.w
        if mouse[1] < scroll_area_size:
            self.y_pos = self.y_pos - scroll
            if self.y_pos < 0:
                self.y_pos = 0
        elif mouse[1] > screen_height - scroll_area_size: 
            self.y_pos = self.y_pos + scroll
            if self.y_pos > (self.world.area.h * self.hex_size()) - self.map_area.h:
                self.h_pos = (self.world.area.h * self.hex_size()) - self.map_area.h

    def process_event(self, event):
        pass
