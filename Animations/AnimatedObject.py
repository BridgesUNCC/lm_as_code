

class AnimatedObject:
    name = None
    animations = None
    
    def __init__(self, name: str):
        self.name = name
        self.animations = []

    def initial(self):
        '''
        return the object representing the initial state of the animated object
        '''
        return {"name": self.name}

    def base_animation_step(self) -> dict:
        
        return {"applyon": self.name}
    
    def flush_animations(self) -> list[dict]:
        '''
        This should return all the animations and change of states that have been conducted on the animated object. And flush them.
        '''
        to_ret = self.animations
        self.animations = []
        return to_ret
