from manim import *
import random
from typing import override
import json
import sys


class Renderer(Scene):
    def construct(self):
        r = Rectangle()
        self.add(r)
        
        self.play (r.animate.shift([1., 1., 0.])) # what kind of scale
        # is this that's right manim viewport is [-4;+4] in y axis not
        # [-1;+1].
        #
        # but it's [-5.something; +5.something] on the x-axis.
        #
        # I guess they wanted to maintain some kind of screen
        # coordinate equivalent so that (+1,0) and (0,+1) are the same
        # number of pixels.
        #
        # This behavior is editable through the config through. Check ManimConfig.frame_y_radius for instance.
                
  
if __name__ == '__main__':
    config.pixel_height = 1080
    config.pixel_width = 1920
    
    scene = Renderer()
    scene.render() # That's it!
          
        
        
        
        

