import pygame
from world import World

class State:
    def enter(self):
        """Called when you enter a new state"""
        pass

    def exit(self):
        """Called when a state is discarded"""
        pass

    def pause(self):
        """Called when another state is pushed into the stack"""
        pass

    def resume(self):
        """Called when a state is popped and this one has to continue"""
        pass

    def update(self, proportion):
        """Provide method to update this state"""
        pass

    def draw(self, screen):
        """Provide method to paint this state in the screen"""
        pass

    def process_event(self, event):
        """Provide method to process an event"""
        pass

class WorldState(State):
    def enter(self):
        self.world = World()

    def update(self, proportion):
        self.world.update(proportion)

    def draw(self, screen):
        self.world.draw(screen)

    def process_event(self, event):
        self.world.process_event(event)
