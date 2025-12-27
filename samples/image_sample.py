from typing import override
import json
import sys
from Animations.MasterAnimation import *
from Animations.Image import *




if __name__ == "__main__":
    my_master_anim = MasterAnimation() #This is the main interface object

    my_img = Image("img", "samples/img1.png")

    my_master_anim.addAnimatedObject("img", my_img)

    my_img.change_to("samples/img2.png")

    my_master_anim.step()

    # output
    data = my_master_anim.complete_animation_object()

    json_str = json.dumps(data, indent=2)
    with open(sys.argv[1], "w") as out:
        out.write(json_str)

    
