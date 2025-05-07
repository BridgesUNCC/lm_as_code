import pyglet
from pyglet import shapes
import os
import networkx.drawing.layout 
from Templates.GraphTemplate import graphPopulation

user_path=pyglet.resource.get_data_path('InteractiveManim/configs')
if not os.path.exists(user_path): os.makedirs(user_path)
print(user_path)


window=pyglet.window.Window(800,600,"Manim interaction tests")

start_x,start_y=0,0
#Simple test input box for saving to json
initial_input_box=pyglet.gui.TextEntry(
text="Enter node",
x=100,
y=100,
width=50
)
@window.event
def on_mouse_press(x,y,button,modifiers):
    global dragging,start_x,start_y 
    dragging=True
    start_x=x
    start_y=y
@window.event
def on_mouse_release(x,y,button,modifiers):
    global dragging
    dragging=False

def on_mouse_drag(x,y,dx,dy,button,modifiers):
    global dragging,start_y,start_x
    if dragging:
        pass #Fix
@window.event('initial_input_box')
def show_text_box():
    initial_input_box.event()
def run_app(): 
    pyglet.app.run()

def main():
    
    run_app
if __name__ == "__main__":
    from manim import config

    config.media_width = "100%"
    run_app()