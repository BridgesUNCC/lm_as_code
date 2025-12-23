from AnimatedObject import AnimatedObject
from manim import *
import networkx as nx
from networkx.algorithms import tree



class TTS(AnimatedObject):
    
    def __init__ (self, renderer, data):
        '''
        render is a reference to the Renderer object
        
        data should be all the configuration for that TTS voice. Currently none, so we ignore it.
        '''
        AnimatedObject.__init__(self, renderer)

    
    def animate(self, action:dict) -> list[Animation]:
        '''
        All actions should have one field: "type"

        For type "say", the action should have the field "text" which should be a string with the text to say.
        '''
        if action["type"] == "say":
            text = action["text"] #todo check for string type
            return [ ]
        AnimatedObject.animate(self, action)
        

    
