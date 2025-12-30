from manim import *
import random
from typing import override
import json
import sys


class Renderer(Scene):
    def construct(self):
        r = Rectangle()
        g = VGroup()
        g.add(r)
        self.add(g)
        
        self.play (g.animate.shift([2., 2., 0.]))

        self.play (g.animate.add(Circle())) #This create a Circle centered at (0,0) even though the circle is part of teh group and the group has shifted.
        #This does not work like a SVG <g> group that retain transformation. Or a node in a scene graph

        #The only thing the group does is that it will forward the operations to BOTH obects now. For instance, this will shift both objects
        self.play (g.animate.shift([1., 1., 0.]))
        
        
        
                
  
if __name__ == '__main__':
    config.pixel_height = 1080
    config.pixel_width = 1920
    
    scene = Renderer()
    scene.render() # That's it!
          
        
        
        
        

