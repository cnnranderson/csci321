from utilities import *

class State():
    """A state that does nothing."""
    def __init__(self, obj): 
        self.obj = obj

    ## All states should respond to these:
    def enter(self): pass
    def execute(self): pass
    def exit(self): pass

    def change_state(self, newstate):
        obj = self.obj
        obj.state.exit()
        obj.state = newstate
        obj.state.enter()

class GameState(State):
    """A state for simple Game Maker type games,
       used with corresponding GameObject class.
       updates velocity with gravity and friction,
       updates animation
       Methods to override:
          update_begin
          update_middle
          update_end
          animation_end"""

    def execute(self):
        obj = self.obj
        obj.previouspos = obj.pos
        self.update_begin()
        self.update_velocity()
        obj.pos += obj.velocity
        self.update_middle()
        obj.rect.center = obj.pos
        self.update_end()
        self.update_animation()

    def update_velocity(self):
        obj = self.obj
        obj.velocity += obj.gravity
        obj.velocity -= obj.friction * obj.velocity
        ## fake static friction
        if obj.friction > 0 and norm(obj.velocity) < 0.1:
            obj.velocity *= 0
  
    def update_animation(self):
        obj = self.obj
        obj.frame += obj.aspeed
        if obj.frame >= obj.strip.nframes-1:
            self.animation_end()
        obj.frame %= obj.strip.nframes
        obj.image = obj.strip.images[int(obj.frame)]

    ## Overridable to change behavior:
    def update_begin(self): pass
    def update_middle(self): pass
    def update_end(self): pass
    def animation_end(self): pass



