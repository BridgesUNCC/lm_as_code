from Animations.AnimatedObject import *

class Image(AnimatedObject):
    filepath_base = None
    
    def __init__(self, name:str, filepath:str):
        super().__init__(name)
        #check existance?
        self.filepath_base = filepath
    
    def initial(self):
        ret = super().initial()
        ret ["type"] = "image"
        ret ["data"]["base"] = self.filepath_base
        return ret

    def change_to(self, filepath: str):
        stuff = self.base_animation_step()
        stuff["data"] = {"type":"change_to", "filepath": filepath}
                
        self.animations.append(stuff)
        
