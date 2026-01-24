from manim import Animation
from manim import VGroup
from manim import Group
from manim import FadeIn
from manim import FadeOut


class AnimatedObject:
    renderer = None
    group = None
    
    
    def __init__ (self, renderer):
        self.renderer = renderer
        self.group = Group()
        self.renderer.add(self.group)
    
    def animate(self, action:dict) -> list[Animation]:
        '''
        animate will return a list of manim animations that will be played at the same time.
        
        Derived class should always call their parent class for actions they do not know how to handle.

        action is nested dictionary, usually coming from a JSON object, that indicate what the animation should.
        action is guaranteed to have a "type" field that is a string. It is used to determine what kind of animation this action represents.
        action may contain other fields as defined by downstream types of AnimatedObject

        TODO: should specify what kind of exception thrown
        '''
        if action["type"] == "fadeout":
            return [ FadeOut(self.group) ]

        if action["type"] == "fadein":
            return [ FadeIn(self.group) ]

        if action["type"] == "scale":
            ratio = action["ratio"]
            return [ self.group.animate.scale(ratio) ]
        
        if action["type"] == "translate":
            normalized = action["vector"]
            for i in range(3):
                normalized[i] *= 4 #stupid manim coordinate system
            return [ self.group.animate.shift(normalized) ]

        if action["type"] == "matrixtransform":
            mat = action["matrix"]
            return [ self.group.animate.apply_matrix(mat) ]
            
        
        raise "WTF"
