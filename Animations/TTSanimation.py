from Animations.AnimatedObject import *

class TTSanimation(AnimatedObject):

    def __init__(self, name: str):
        super().__init__(name)
        self.init_hidecamera()
    
    def initial(self):
        ret = super().initial()
        ret ["type"] = "tts"
        return ret

    def say(self, text: str):
        stuff = self.base_animation_step()
        stuff["data"] = {"type":"say", "text": text}
                
        self.animations.append(stuff)
        
