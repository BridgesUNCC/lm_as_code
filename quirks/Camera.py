from manim import *

class RestrictedCamera(MovingCamera):
    def __init__(self, *args, **kwargs):
        self.only_render = kwargs.pop("only_render", [])
        super().__init__(*args, **kwargs)

    def capture_mobjects(self, mobjects, **kwargs):
        # We filter the global mobject list to only include 
        # what this camera is allowed to see.
        #self.pixel_array.fill(0)
        self.reset()
        filtered_mobjects = [m for m in mobjects if m in self.only_render]
        #print (len(filtered_mobjects))
        super().capture_mobjects(filtered_mobjects, **kwargs)

class ProfessionalMultiCamera(Scene):
    def construct(self):
        # 1. Create objects ALL AT THE CENTER (no shifting needed)
        sq = Square(color=BLUE)
        tri = Triangle(color=RED)
        circ = Circle(color=GREEN)
       
        ta = Text("a")
        tb = Text("b")

        rect = Rectangle(color=BLUE, width=20, height=8, fill_color=BLUE, fill_opacity=1.)
        rect.set_z_index(2)
        # We add them to the scene so they exist in the "world"
        #self.add(sq, tri, circ)

        cam_config = {
            "pixel_height": config.pixel_height,
            "pixel_width": config.pixel_width,
            "frame_height": config.frame_height,
            "frame_width": config.frame_width,
        }

        # 2. Setup Cameras with "Whitelists"
        # Each camera is told exactly which mobject it is allowed to see
        cam_a = RestrictedCamera(only_render=[sq], **cam_config)
        cam_b = RestrictedCamera(only_render=[tri], **cam_config)
        cam_c = RestrictedCamera(only_render=[circ], **cam_config)

        # 3. Create the Display Viewports
        view_a = ImageMobjectFromCamera(cam_a)
        view_b = ImageMobjectFromCamera(cam_b)
        view_c = ImageMobjectFromCamera(cam_c)

        # Arrange viewports side-by-side
        viewports = Group(view_a, ta, view_b, tb, view_c).arrange(RIGHT, buff=0.5)
        viewports.set_width(config.frame_width - 1)
        viewports.set_z_index(3)
        self.add(rect)
        self.add(viewports)

        self.add_updater(lambda dt: cam_a.capture_mobjects(self.mobjects))
        self.add_updater(lambda dt: cam_b.capture_mobjects(self.mobjects))
        self.add_updater(lambda dt: cam_c.capture_mobjects(self.mobjects))

        # 4. Animate everything at once
        # Even though they are at the same coordinates, 
        # the viewports only show their assigned object.
        self.play(
            sq.animate.shift(UP),
            tri.animate.rotate(PI),
            circ.animate.scale(1.5),
            run_time=2
        )
        self.play(sq.animate.rotate(PI/2))
        self.wait()

pmc = ProfessionalMultiCamera()
pmc.render()

