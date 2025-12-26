from manim import *
import random
from typing import override
import json
import sys
from AnimatedObject import AnimatedObject
from TTSanimation import TTSanimation
from NetworkXGraph import NetworkXGraph


        
class Renderer(Scene):
    '''
    Renderer is a manim scene
    '''
    animation_steps = None
    objects = {}

    def setup(self):
        '''this expects that an inputfilename is populated in self.datafile.
        this file should be JSON format and contain a dict the dict
        should be formated as this where "initial" is a dictionary of
        AnimationObject and animation is a list of animation step
        
        {
        "initial": { ...
          },
        "animation": [ ...
          ]
        }

        initial is a dictionary. The dictionary give names to
        animation objects. names are string. The animation object are
        defined by a type which is a string and a data object used to
        construct the animation object.

        {
        name: {
          "type" : str,
          "data" : some data
          }
        }


        animation is a list of animation step. Each animation step is
        a list of actual actions. Each step executes all the
        actions at the same time.

        actions are dictionaries with two fields: "applyon" and
        "data". applyon indicates which AnimationObject is impacted by
        the action and data is parameters to pass to the
        AnimationObject.animate function

        {
          "applyon": name,
          "data": some data
        }

        '''
        with open(self.datafile) as inputfile:
            data = json.load(inputfile)
            initialdata = data["initial"]
            
            for key, value in initialdata.items():
                print (key, value)
                #TODO check key is string
                if value["type"] == "nx":
                    self.objects[key] = NetworkXGraph(self, value["data"])

                if value["type"] == "tts":
                    self.objects[key] = TTSanimation(self, value["data"])

                    
            self.animation_steps = data["animation"]
        
    def construct(self):
        #Animation.
        for animation_step in self.animation_steps:
            the_actions = []
            for action in animation_step:
                applyon = action["applyon"] #TODO check for string
                data = action["data"]
                the_actions.extend(self.objects[applyon].animate(data)) #should catch exception and generate easier to interpret error message
            self.play (the_actions)
                
  
if __name__ == '__main__':
    config.pixel_height = 1080
    config.pixel_width = 1920
    
    scene = Renderer()
    scene.datafile = sys.argv[1]
    scene.render() # That's it!
          
        
        
        
        

