from manim import Animation
from manim import VGroup
from manim import Group
from manim import FadeIn
from manim import FadeOut

from manim import MovingCamera
from manim import config
from manim import ImageMobjectFromCamera

class AnimatedObject:
    renderer = None
    group = None
    camera = None
    view_buffer = None
    
    def __init__ (self, renderer, data = None):
        self.renderer = renderer
        self.group = Group()
        self.renderer.add(self.group)

        ## Setup Camera logic
        cam_config = {
            "pixel_height": config.pixel_height,
            "pixel_width": config.pixel_width,
            "frame_height": config.frame_height,
            "frame_width": config.frame_width,
        }
        self.camera = RestrictedCamera(only_render=[self.group], **cam_config)
        self.view_buffer = ImageMobjectFromCamera(self.camera)

        self.view_buffer.set_width(config.frame_width-1)
        self.view_buffer.set_z_index(1000)
        
        self.renderer.add(self.view_buffer)

        self.renderer.add_updater(lambda dt: self.camera.capture_mobjects())
        
    def style_camera(self, renderer, data) :
        if "hidecamera" in data:
            if data["hidecamera"]:
                print ("hiding")
                self.view_buffer.move_to ([100., 100., 0.]) #that's hacky but that should work    
        if "location" in data:
            loc = data["location"]
            #TODO assert 4 floats
            #format top, left, bottom, right
            top = loc[0]
            left = loc[1]
            bottom = loc[2]
            right = loc[3]
            h = top - bottom
            w = right - left
            #this probably doesn't do exactly what you asked but should keep aspect ratio consistent, maybe?
            self.view_buffer.height = h
            self.view_buffer.width = w
            self.view_buffer.move_to([left+w/2, bottom+h/2, 1000]) #move_to is center based
            
        
    def animate(self, action:dict) -> list[Animation]:
        '''
        animate will return a list of manim animations that will be played at the same time.
        
        Derived class should always call their parent class for actions they do not know how to handle.

        action is nested dictionary, usually coming from a JSON object, that indicate what the animation should.
        action is guaranteed to have a "type" field that is a string. It is used to determine what kind of animation this action represents.
        action may contain other fields as defined by downstream types of AnimatedObject

        TODO: should specify what kind of exception thrown
        '''
        if action["type"] == "fadeout":
            return [ FadeOut(self.group) ]

        if action["type"] == "fadein":
            return [ FadeIn(self.group) ]

        if action["type"] == "scale":
            ratio = action["ratio"]
            return [ self.group.animate.scale(ratio) ]
        
        if action["type"] == "translate":
            normalized = action["vector"]
            for i in range(3):
                normalized[i] *= 4 #stupid manim coordinate system
            return [ self.group.animate.shift(normalized) ]

        if action["type"] == "matrixtransform":
            mat = action["matrix"]
            return [ self.group.animate.apply_matrix(mat) ]
            
        
        raise "WTF"


    
class RestrictedCamera(MovingCamera):
    def __init__(self, *args, **kwargs):
        self.only_render = kwargs.pop("only_render", [])
        super().__init__(*args, **kwargs)

    def get_all_mobjects_recursive(self, group):
        all_mobjects = []
    
        for item in group.submobjects:
            all_mobjects.append(item)
            # Check if the item has submobjects (meaning it's a Group or VGroup)
            if len(item.submobjects) > 0:
                # Recursively extend the list with items from the sub-group
                all_mobjects.extend(self.get_all_mobjects_recursive(item))
            
        return all_mobjects

        
    def capture_mobjects(self, **kwargs):
        self.reset()

        # We only render what this camera is allowed to see.

        #print (len(filtered_mobjects))
        all_mobs_in_only_render = []
        for a in self.only_render:
            all_mobs_in_only_render.extend(self.get_all_mobjects_recursive(a))

        #print (f"all mobs in only render: {len(all_mobs_in_only_render)}")
            
        super().capture_mobjects(all_mobs_in_only_render, **kwargs)
