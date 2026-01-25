from AnimatedObject import AnimatedObject
from manim import *
from TTS.api import TTS
import wave
import contextlib
import torch

class TTSanimation(AnimatedObject):
    tts = None

    def get_duration_wave(self, file_path):
        with contextlib.closing(wave.open(file_path,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration
        return 0.1 #WTF
    
    def __init__ (self, renderer, data):
        '''
        render is a reference to the Renderer object
        
        data should be all the configuration for that TTS voice. Currently none, so we ignore it.
        '''
        AnimatedObject.__init__(self, renderer)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

        
    
    def animate(self, action:dict) -> list[Animation]:
        '''
        All actions should have one field: "type"

        For type "say", the action should have the field "text" which should be a string with the text to say.
        '''
        if action["type"] == "say":
            text = action["text"] #todo check for string type
            hashcode = hash(text) #if there are more parameter, should hash on them too.
            #python built in hash function is salted; so no caching
            path_to_wav = "media/audio/"+str(hashcode)+".wav"
            console.log("text: " +text)
            self.tts.tts_to_file(text=text,
                                 speaker=self.tts.speakers[0],
                                 language="en",
                                 file_path=path_to_wav)
            self.renderer.add_sound(path_to_wav)

            # hacky stuff, to make the sound cached right
            wait_anim = animation.animation.Wait(self.get_duration_wave(path_to_wav), frozen_frame=False)
            text = Text(path_to_wav)
            text.set_opacity(0.0)
            wow = Create(text)
            
            return [ wow, wait_anim ]
        AnimatedObject.animate(self, action)
        

    
