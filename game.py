import sys, pygame
from world import World
from world_state import WorldState
from area_state import AreaState
from constants import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.size = width, height = screen_width, screen_height
        self.screen = pygame.display.set_mode(self.size)
        self.states = []
        self.exit = False

    def push_state(self, state):
        if len(self.states):
            self.states[-1].pause()
        self.states.append(state)
        state.enter()

    def top_state(self):
        return self.states[-1]

    def pop_state(self):
        if len(self.states):
            self.states[-1].exit()
            self.states.pop()
        if len(self.states):
            self.states[-1].resume()
        else:
            self.exit = True

    def start(self):
        self.world = World('wesnoth.world')
        self.world_state = WorldState(self)

        self.area_state = AreaState(self)
        self.area_state.set_area(self.world.get_start_area())

        self.push_state(self.world_state)
        self.push_state(self.area_state)
        self.loop()

    def loop(self):
        #time is specified in milliseconds
        #fixed simulation step duration
        step_size = 10
        #max duration to render a frame
        max_frame_time = 100

        now = pygame.time.get_ticks()-1
        frames = 0
        time = 0
        while not self.exit:
            #handle events
            for e in pygame.event.get():
                #print str(e)
                if e.type == pygame.QUIT:
                    self.exit = True
                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_ESCAPE:
                        self.pop_state()
                    if self.exit:
                        break
                    self.top_state().process_event(e)
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.top_state().process_event(e)

            if self.exit:
                break

            #get the current real time
            t = pygame.time.get_ticks()

            #if elapsed time since last frame is too long...
            if t - now > max_frame_time:
                #slow the game down by resetting clock
                now = t - step_size
                #alternatively, do nothing and frames will auto-skip, which
                #may cause the engine to never render!

            #this code will run only when enough time has passed, and will
            #catch up to wall time if needed.
            while(t-now > step_size):
                #save old game state, update new game state based on step_size
                now += step_size
            else:
                pygame.time.wait(10)

            #render game state. use 1.0/(step_size/(T-now)) for interpolat
            self.top_state().update(1.0/(step_size/(t-now)))
            if frametime_enabled:
                before = pygame.time.get_ticks()
            self.top_state().draw(self.screen)
            if frametime_enabled:
                after = pygame.time.get_ticks()
                frames = frames + 1
                time = time + (after-before)
            pygame.display.flip()

        if frametime_enabled:
            print 'average render time: %f' % (float(time)/frames)
