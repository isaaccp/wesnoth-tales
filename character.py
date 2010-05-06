import pygame

class Character:
    def __init__(self, name):
        self.name = name
        self.x = None
        self.y = None
        self.unique = None
        self.image = pygame.image.load('images/units/%s.png' % name)

    def set_location(self, x, y):
        self.x = x
        self.y = y
