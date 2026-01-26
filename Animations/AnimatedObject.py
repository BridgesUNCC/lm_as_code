

class AnimatedObject:
    name = None
    animations = None
    camera = None
    
    def __init__(self, name: str):
        self.name = name
        self.animations = []
        self.camera={}

    def init_hidecamera(self):
        self.camera["hidecamera"] = True

        
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

    def move_camera(self, location):
        # assert location is 4 uple [top, left, bottom, right]
        
        stuff = self.base_animation_step()
        stuff["data"] = {"type":"movecamera",
                         "location": location
                         }
        self.animations.append(stuff)

    def hide_camera(self, hidden=True):
        stuff = self.base_animation_step()
        stuff["data"] = {"type":"hidecamera",
                         "hidecamera": hidden
                         }
        self.animations.append(stuff)

    def show_camera(self):
        return self.hide_camera(False)
    
    def flush_animations(self) -> list[dict]:
        '''
        This should return all the animations and change of states that have been conducted on the animated object. And flush them.
        '''
        to_ret = self.animations
        self.animations = []
        return to_ret
