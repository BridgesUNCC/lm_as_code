

class MasterAnimation:
    '''
    this class is meant to be the primary object that contains teh entire animations
    '''

    objects = None

    anims = None
    
    def __init__(self):
        self.objects = {}
        self.anims = []
    
    def addAnimatedObject(self, name: str, obj:AnimatedObject):
        #TODO check existing + exception
        #if name not str exception
        self.objects[name] = obj

    def initial(self): #is there a reason for this to be public?
        base = {}
        for o in self.objects:
            base[o] = self.objects[o].initial()
        return base

    def animation(self): #is there a reason for this to be public?
        '''
        return the json that goes in the serialization for renderer
        '''
        return anims

    def complete_animation_object(self):
        '''
        returns the json that is a complete animation object
        '''
        data = { "initial": self.initial(),
                 "animation": self..animation()}


    def step(self):
        '''
        call this for each step of the animation
        '''
        cur = []
        for o in objects:
            cur = cur + self.objects[o].flush_animations() # which function is inplace list append?
        
        self.anims.append(cur)
