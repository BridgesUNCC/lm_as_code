import random
from typing import override
import json
import sys
from Animations.TTSanimation import *
from Animations.MasterAnimation import *


                



if __name__ == "__main__":
    my_master_anim = MasterAnimation() #This is the main interface object

    #set up the animation objects we need
    tts = TTSanimation("tts")
    
    my_master_anim.addAnimatedObject("tts", tts)

    #actually build the animation
    tts.say(f"Saying something")
    my_master_anim.step()

    var = "variable"
    
    tts.say(f"Saying something else with a {var}")
    my_master_anim.step()

    

    # output
    data = my_master_anim.complete_animation_object()
    
    json_str = json.dumps(data, indent=2)
    with open(sys.argv[1], "w") as out:
        out.write(json_str)

    
