from manim import *
import random
from typing import override
import json
import sys


class Renderer(Scene):
    def construct(self):
        r = Rectangle()
        self.add(r)
        
        self.play (r.animate.scale(.5)) # one can scale
        
        self.play (r.animate.shift([1., 1., 0.])) #one can shift

        self.play ([r.animate.scale(.5), r.animate.shift([1., 1., 0.])]) #but one can't shift AND scale
        

                
  
if __name__ == '__main__':
    config.pixel_height = 1080
    config.pixel_width = 1920
    
    scene = Renderer()
    scene.render() # That's it!
          
        
        
        
        

