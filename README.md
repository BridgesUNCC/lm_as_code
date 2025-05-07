# manim_project
Basic info: 
    
To run: 
Need to have UV installed, https://docs.manim.community/en/stable/installation.html
other packages needed: pyglet, IPython, numpy, networkx
To run the project do: uv run manim Tests/InteractivityTest.py -p --renderer=opengl


To run BFSAnim:
cd .\Templates\
manim -pqm GraphTemplate.py BFSAnim --renderer=opengl

BFSAnim Notes:
Set input mode to 0 for keyboard input, 1 for mouse input. When running the program 
use keyboard to input answer choices or mouse to select the node that will be traversed next.

