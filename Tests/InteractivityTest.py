from manim import *
import networkx as nx
from manim.opengl import *
import pyglet
import random
from pyglet.window import mouse
import numpy as np
from Assignment import Assignment
class GraphTemp2(MovingCameraScene,Assignment): 
    locations={}
    last_node=None
    correct_node = None
    incorrect_counter = 0
    incorrect_max = 3
    question_text = None
    feedback_text = None  
    assignments=[]
    current_assignment_index=0
    def construct(self):
        self.zoom_scale=0.75
        #Variable n defines number of nodes.
        n = 9
        nodes = [i for i in range(n)]
        edges = []
        #Populating edges array.
        for i in range(n-1):
            if(i+1 >= n):
                continue
            c1 = (i, i+1)
            edges.append(c1)
            if(i+2 >= n):
                continue
            c2 = (i, i+2)
            edges.append(c2)
        #Randomizing the position of nodes.
        self.pos = {i: (random.randint(-2,2), random.randint(-2,2), 0) for i in range(n)}
        self.locations=self.pos
        #Creating graph mobject.
        self.G = Graph(
            nodes, 
            edges, 
            layout = self.pos,
            layout_config = {"space_x": 10, "space_y": 10},
            layout_scale = 0.25,
            labels = True,
            label_fill_color= 'BLUE'
        )
        self.highlight_circle = Circle(radius=0.25)
        #self.add(self.highlight_circle)
        self.original_width = self.camera.scale
        self.add(self.G)
        self.remove_highlight=None
        self.original_scale=self.camera.scale

        self.is_assignment=True
        self.assignments = [
            (1, "Select the first node."),
            (3, "Select the third node."),
            (5, "Select the fifth node."),
            (7, "Select the seventh node.")]
        self.start_next_assignment()


        self.interactive_embed()

    def on_key_press(self,symbol,modifiers):
            if symbol == pyglet.window.key._1:
                if 1 in self.pos:
                    self.play(
                    self.camera.animate.scale(0.5).move_to(self.pos[1]),
                    FadeOut(self.highlight),
                    FadeIn(Circle(radius=0.25).move_to(self.pos[1]))  
                )
            if symbol==pyglet.window.key.MINUS:
                 self.camera.scale((1/self.zoom_scale)).move_to(ORIGIN)

            super().on_key_press(symbol, modifiers)


    def on_mouse_press(self, point, button, modifiers):
            
            x,y,z=point
            scene_x=x
            scene_y=y
            
            print(x,y)
            #if self.last_node is not None: 
             #   scene_x,scene_y,_=self.calculate_relative_node_pos(self.last_node,self.zoom_scale)
            
            rounded_x = round(scene_x, 0)
            rounded_y = round(scene_y, 0)
            if rounded_x==-0.0:rounded_x=0.
            if rounded_y == -0.0:rounded_y=0.
            print(rounded_x,rounded_y)
            
            for node, pos in self.pos.items():
                if (round(pos[0], 0), round(pos[1], 0)) == (rounded_x, rounded_y):
                    
                    #self.focus_node(node)
                    
                    Assignment.check_answer(node)
                    
            super().on_mouse_press(point, button, modifiers)

    def focus_node(self,node):
        '''if self.last_node is not None and self.last_node!=node:
            self.play(self.camera.animate.scale(1/self.zoom_scale).move_to(ORIGIN))'''
        

        self.highlight_circle.move_to(self.pos[node])
        

        self.play(
                #self.camera.animate.scale(1).move_to(self.pos[node]),
                FadeIn(self.highlight_circle))
        self.last_node = node
    