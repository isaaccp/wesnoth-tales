import pygame
from location import Location
from constants import *

class Display:
    layers = ('TERRAIN', 'UNIT')

    def __init__(self, world):
        self.world = world
        self.map_area = pygame.Rect(0, 0, 640, 640)
        self.zoom = tile_size
        self.x_pos = 0
        self.y_pos = 0
        self.cursors = {}
        for c in ['normal', 'select-location', 'move', 'attack']:
            self.cursors[c] = pygame.image.load('images/cursors/%s.png' % c)

        self.cursor = self.cursors['normal']
        self.current = pygame.image.load('images/terrain/cursor.png')
        self.select = pygame.image.load('images/terrain/select.png')
        self.grid = pygame.image.load('images/terrain/grid.png')

        self.footsteps = {}
        for s in ['in', 'out']:
            for d in ['n', 'ne', 'se', 's', 'nw', 'sw']:
                steps = '%s-%s' % (s, d)
                image = 'images/footsteps/foot-normal-%s.png' % steps
                self.footsteps[steps] = pygame.image.load(image)

        #current selection
        self.selection = None

        #current path
        self.path = None
        self.path_images = None

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

    def get_absolute_location_x(self, loc): 
        return self.map_area.x + loc.x * self.hex_width()

    def get_absolute_location_y(self, loc):
        y = self.map_area.y + loc.y * self.zoom
        if (loc.x % 2) == 1:
            return y + self.zoom/2
        else:
            return y

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

    def center_view(self):
        loc = self.world.area.characters[0].location()
        x = self.get_absolute_location_x(loc)
        y = self.get_absolute_location_y(loc)

        self.x_pos = x - screen_width/2
        self.y_pos = y - screen_height/2

    def draw(self, screen):
        area = self.world.area
        screen.fill((0,0,0))
        loc1 = self.pixel_position_to_hex((0,0))
        loc2 = self.pixel_position_to_hex((self.map_area.w, self.map_area.h))
        loc2.x = loc2.x + 1
        loc2.y = loc2.y + 1
        for l in (loc1, loc2):
            if l.x < 0:
                l.x = 0
            elif l.x >= area.w:
                l.x = area.w - 1
            if l.y < 0:
                l.y = 0
            elif l.y >= area.h:
                l.y = area.h - 1
        font = pygame.font.SysFont("Courier New",14)
        clip_rect = screen.set_clip(self.map_area)
        for l in ['flat', 'volume', 'debug']:
            cur_layer = '%s_image' % l
            for i in range(loc1.x, loc2.x + 1):
                for j in range(loc1.y, loc2.y + 1):
                    t = area.map[i][j]
                    loc = Location(i, j)
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

        for c in area.characters:
            r = self.rect(c.image, c.loc)
            screen.blit(c.image, r)
        
        mouse = pygame.mouse.get_pos()
        loc = self.pixel_position_to_hex(mouse)

        r = self.rect(self.current, loc)
        screen.blit(self.current, r)

        if self.selection:
            self.path = area.can_move(self.selected_unit(), loc)
            if self.path:
                self.calculate_path_images()
                self.cursor = self.cursors['move']
                for pair in range(len(self.path_images)/2):
                    l = self.path[pair]
                    for i in range(2):
                        img = self.path_images[pair*2+i]
                        if img:
                            r = self.rect(img, l)
                            screen.blit(img, r)
            else:
                self.cursor = self.cursors['normal']
            r = self.rect(self.select, self.selection)
            screen.blit(self.select, r)
        else:
            self.cursor = self.cursors['normal']

        r = mouse
        screen.blit(self.cursor, r)
                        
        screen.set_clip(clip_rect)

    def update(self, proportion, new_area):
        if new_area:
            self.center_view()
        else:
            #scroll
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            loc = self.pixel_position_to_hex(event.pos)
            if event.button == 1:
                if not self.selection:
                    if self.world.area.map[loc.x][loc.y].has_key('character'):
                        self.set_selection(loc)
                else:
                    unit = self.selected_unit()
                    path = self.world.area.can_move(unit, loc)
                    if path:
                        unit.move(path)
                        self.set_selection(None)
            elif event.button == 3:
                if self.selection:
                    self.selection = None
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_c:
                self.center_view()

    def set_selection(self, loc):
        self.selection = loc

    def selected_unit(self):
        loc = self.selection
        return self.world.area.map[loc.x][loc.y]['character']

    def calculate_path_images(self):
        self.path_images = []
        area = self.world.area
        path = self.path
        sense = ['in', 'out']
        for i, t in enumerate(path):
            for h in range(2):
                if i == 0 and h == 0:
                    self.path_images.append(None)
                    continue
                if i == len(path)-1 and h == 1:
                    self.path_images.append(None)
                    continue
                direction = path[i+h].relative_dir(path[i+(h-1)])
                steps = '%s-%s' % (sense[h], direction)
                self.path_images.append(self.footsteps[steps])
