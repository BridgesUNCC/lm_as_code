from manim import *
import random
import networkx as nx
from typing import override
from networkx.algorithms import tree
import json
import sys

class Renderer(Scene):
    sceneNXGraph = None
    animation_steps = None

    def setup(self):
        with open(self.datafile) as inputfile:
            data = json.load(inputfile)
            self.sceneNXGraph = nx.node_link_graph(data["initial"])
            self.animation_steps = data["animation"]
        
    def construct(self):
        the_pos = {v: self.sceneNXGraph.nodes[v]["pos"] for v in self.sceneNXGraph}
        
        sceneGraph = Graph.from_networkx(self.sceneNXGraph, 
                                         layout = the_pos, 
                                         labels = True, #Vertex labels
                                         label_fill_color = BLUE,
                                         layout_scale = 4.0, 
                                         edge_type = DashedLine)
        
        #Weight population
        weightedEdgesArr = [(edge[0], edge[1], self.sceneNXGraph.edges[edge]["weight"]) for edge in self.sceneNXGraph.edges()]

        
        #Weight label mobject creation & positioning.
        edgeLabels = VGroup()
        for wEdge in weightedEdgesArr:
            edge = (wEdge[0],wEdge[1])
            weight = wEdge[2]
            edgeLine = sceneGraph.edges[edge]
            label = Text(str(weight)).scale(0.75)
            center = edgeLine.get_center()
            label.move_to(center)
            edgeLabels.add(label)

                
        #Animation.
        self.add(sceneGraph, edgeLabels)

        for animation_step in self.animation_steps:
            the_actions = []
            for action in animation_step:
                if action["type"] == "edgecolor":
                    edge=None
                    try:
                        temp = (action["src"], action["dst"])
                        edge = sceneGraph.edges[temp]
                    except KeyError as e: #this is normal in undirected graph
                        temp = (action["dst"], action["src"])
                        edge = sceneGraph.edges[temp]
                        
                    the_actions.append(edge.animate.set_color(ManimColor(action["color"])))
                if action["type"] == "vertexcolor":
                    the_actions.append (sceneGraph.vertices[action["vertex"]].animate.set_color(ManimColor(action["color"])))
            self.play (the_actions)
                
            
  
if __name__ == '__main__':
    scene = Renderer()
    scene.datafile = sys.argv[1]
    scene.render() # That's it!
          
        
        
        
        

