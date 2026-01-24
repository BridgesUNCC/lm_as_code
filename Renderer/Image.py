from AnimatedObject import AnimatedObject
from manim import *

class ImageAnimation(AnimatedObject):
    imagemobject = None

    def _scale_me(self):
        # scale to fit screen
        self.imagemobject.scale_to_fit_width(config.frame_width)
        
        if self.imagemobject.height > config.frame_height:
            self.imagemobject.scale_to_fit_height(config.frame_height)
        
    
    def __init__ (self, renderer, data):
        '''
        render is a reference to the Renderer object
        
        data should be all the configuration for that image
        '''
        AnimatedObject.__init__(self, renderer)
        
        #TODO: check existance
        self.imagemobject = ImageMobject(data["base"])

        #TODO: should this be a parameter?
        self._scale_me()
        self.group.add(self.imagemobject)
        
    
    def animate(self, action:dict) -> list[Animation]:
        '''
        All actions should have one field: "type"

        '''
        
        if action["type"] == "change_to":
            #TODO: check existance
            rets = []
            #  Turns out manim image does not let you update. So you need to add and remove instead
            old_im = self.imagemobject
            new_im = ImageMobject(action["filepath"])
            self.group.add(new_im)
            self.group.remove(old_im)
            self.imagemobject = new_im
            self._scale_me()
            rets.append(FadeOut(old_im))
            rets.append(FadeIn(new_im))
            return rets

        # Pass to base object for generic processing
        return AnimatedObject.animate(self, action) 
        

    
