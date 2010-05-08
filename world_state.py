import pygame
from state import State

class WorldState(State):
    def __init__(self, game):
        self.cursor = pygame.image.load('images/cursors/normal.png')
        self.game = game
        self.world = game.world
        self.map = pygame.image.load('images/maps/%s.png' % self.world.map)

    def enter(self):
        pass

    def update(self, proportion):
        pass

    def draw(self, screen):
        screen.blit(self.map, (0,0))
        for a in self.world.main_areas:
            pygame.draw.rect(screen, (255, 0, 0),
                pygame.Rect(a['pos'], a['size']), 2)
        mouse = pygame.mouse.get_pos()
        r = mouse
        screen.blit(self.cursor, r)

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for a in self.world.main_areas:
                    r = pygame.Rect(a['pos'], a['size'])
                    if r.collidepoint(event.pos):
                        area = self.world.get_area(a['area'])
                        self.game.area_state.set_area(area)
                        self.game.push_state(self.game.area_state)
