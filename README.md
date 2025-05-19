# manim_project
Basic info:  
    
To run with UV package manager:   
'-Need to have UV installed, https://docs.manim.community/en/stable/installation.html  
'-packages needed: see requirements.txt  
'-To run the project do: uv run manim Tests/InteractivityTest.py -p --renderer=opengl  


To run BFSAnim:  
'-cd .\Templates\  
'-manim -pqm GraphTemplate.py BFSAnim --renderer=opengl

BFSAnim Notes:  
Set input mode to 0 for keyboard input, 1 for mouse input. When running the program  
use keyboard to input answer choices or mouse to select the node that will be traversed next.  


## Assignment
Assignment is a group of questions, and correct answers. It is limited to multiple choice, free response will not work due to having to generate a new animation with every key press. You can check answer, start next question, generate visible multiple choice options on   screen (guarantees atleast 1 correct), and complete all assignments.  

## Interactivity 

The interactivity is done using the pyglet library, specifically, on_mouse_press which records location of the mouse when clicked. and on_key_press which records key strokes. Currently, only keystrokes OR mouse input is enabled, but can be easily changed. assignment and check_answer are also overriden, but only to add some animations.  


