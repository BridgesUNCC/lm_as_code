from manim import *
import random
import networkx as nx
from typing import override
from networkx.algorithms import tree
import json
import sys

class NetworkXGraph:
    sceneNXGraph = None
    sceneGraph = None
    edgeLabels = None
    renderer = None
    
    def __init__ (self, renderer, data):
        self.renderer = renderer
        self.sceneNXGraph = nx.node_link_graph(data)

        the_pos = {v: self.sceneNXGraph.nodes[v]["pos"] for v in self.sceneNXGraph}
        
        self.sceneGraph = Graph.from_networkx(self.sceneNXGraph, 
                                         layout = the_pos, 
                                         labels = True, #Vertex labels
                                         label_fill_color = BLUE,
                                         layout_scale = 4.0, 
                                         edge_type = DashedLine)
        
        #Weight population
        weightedEdgesArr = [(edge[0], edge[1], self.sceneNXGraph.edges[edge]["weight"]) for edge in self.sceneNXGraph.edges()]

        
        #Weight label mobject creation & positioning.
        self.edgeLabels = VGroup()
        for wEdge in weightedEdgesArr:
            edge = (wEdge[0],wEdge[1])
            weight = wEdge[2]
            edgeLine = self.sceneGraph.edges[edge]
            label = Text(str(weight)).scale(0.75)
            center = edgeLine.get_center()
            label.move_to(center)
            self.edgeLabels.add(label)
            
        self.renderer.add(self.sceneGraph, self.edgeLabels)

    def animate(self, action) -> List[Animation]:
        if action["type"] == "edgecolor":
            edge=None
            try:
                temp = (action["src"], action["dst"])
                edge = self.sceneGraph.edges[temp]
            except KeyError as e: #this is normal in undirected graph
                temp = (action["dst"], action["src"])
                edge = self.sceneGraph.edges[temp]
                        
            return [ edge.animate.set_color(ManimColor(action["color"])) ]
        if action["type"] == "vertexcolor":
            return [ self.sceneGraph.vertices[action["vertex"]].animate.set_color(ManimColor(action["color"])) ]
        raise "WTF"

        
class Renderer(Scene):
    animation_steps = None
    object = None

    def setup(self):
        with open(self.datafile) as inputfile:
            data = json.load(inputfile)
            self.object = NetworkXGraph(self, data["initial"])
            self.animation_steps = data["animation"]
        
    def construct(self):
                
        #Animation.

        for animation_step in self.animation_steps:
            the_actions = []
            for action in animation_step:
                the_actions.extend(self.object.animate(action))
            self.play (the_actions)
                
            
  
if __name__ == '__main__':
    scene = Renderer()
    scene.datafile = sys.argv[1]
    scene.render() # That's it!
          
        
        
        
        

