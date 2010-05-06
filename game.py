import sys, pygame
from state import WorldState
from constants import *

class Game:
    def __init__(self):
        pygame.init()

        self.size = width, height = screen_width, screen_height
        self.screen = pygame.display.set_mode(self.size)
        self.states = [] 
        self.exit = False

    def start(self):
        self.push_state(WorldState())
        self.loop()

    def push_state(self, state):
        if len(self.states):
            self.states[-1].pause()
        self.states.append(state)
        state.enter()

    def pop_state(self):
        if len(self.states):
            self.states[-1].exit()
            self.states.pop()
        if len(self.states):
            self.states[-1].resume()
        else:
            self.exit = True

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
                    self.states[-1].process_event(e)

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
            self.states[-1].update(1.0/(step_size/(t-now)))
            if frametime_enabled:
                before = pygame.time.get_ticks()
            self.states[-1].draw(self.screen)
            if frametime_enabled:
                after = pygame.time.get_ticks()
                frames = frames + 1
                time = time + (after-before)
            pygame.display.flip()

        if frametime_enabled:
            print 'average render time: %f' % (float(time)/frames)
