import pygame

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
