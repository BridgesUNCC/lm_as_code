

class AnimatedObject:
    name = None
    animations = None
    camera = None
    
    def __init__(self, name: str):
        self.name = name
        self.animations = []
        self.camera={}

    def place_camera(self, location):
        # assert location is 4 uple [top, left, bottom, right]
        self.camera["location"] = location
        
    def initial(self):
        '''
        return the object representing the initial state of the animated object
        '''
        return {"name": self.name, "data": {}, "camera": self.camera}

    def base_animation_step(self) -> dict:
        
        return {"applyon": self.name}
    
    def flush_animations(self) -> list[dict]:
        '''
        This should return all the animations and change of states that have been conducted on the animated object. And flush them.
        '''
        to_ret = self.animations
        self.animations = []
        return to_ret
