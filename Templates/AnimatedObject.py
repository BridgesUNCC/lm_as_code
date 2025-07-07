from manim import Animation

class AnimatedObject:
    renderer = None
    
    def __init__ (self, renderer):
        self.renderer = renderer
    
    def animate(self, action:dict) -> list[Animation]:
        '''
        animate will return a list of manim animations that will be played at the same time.
        
        Derived class should always call their parent class for actions they do not know how to handle.

        action is nested dictionary, usually coming from a JSON object, that indicate what the animation should.
        action is guaranteed to have a "type" field that is a string. It is used to determine what kind of animation this action represents.
        action may contain other fields as defined by downstream types of AnimatedObject

        TODO: should specify what kind of exception thrown
        '''
        raise "WTF"
