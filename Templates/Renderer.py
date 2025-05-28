from manim import *
import random
import networkx as nx
from typing import override
from networkx.algorithms import tree
import json
import sys

class AnimatedObject:
    renderer = None
    
    def __init__ (self, renderer):
        self.renderer = renderer
    
    def animate(self, action:dict) -> list[Animation]:
        '''
        animate will return a list of manim animations that will be played at the same time.
        
        Derived class should always call their parent class for actions they do not know how to handle.

        action is nested dictionary, usually coming from a JSON object, that indicate what the animation should.
        action is guaranteed to have a "type" field that is a string. It is used to determine what kind of animation this action represents.
        action may contain other fields as defined by downstream types of AnimatedObject

        TODO: should specify what kind of exception thrown
        '''
        raise "WTF"


class NetworkXGraph(AnimatedObject):
    sceneNXGraph = None
    sceneGraph = None
    edgeLabels = None
    
    def __init__ (self, renderer, data):
        '''
        data is a dict representation of a networkx graph as exported by networkx.node_link_data

        This assumes that each vertex has a "pos" attribute which is a 3d tuple

        This assumes that each vertex has a "weight" attribute to be used as an edge label

        TODO:weight should probably be optional?
        '''
        AnimatedObject.__init__(self, renderer)
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

    def animate(self, action:dict) -> list[Animation]:
        '''
        NetworkXGraph supports the following actions:
        
        {
        "type": "edgecolor",
        "src": the key of a vertex from the networkx graph the object was constructed with,
        "dst": the key of a vertex from the networkx graph the object was constructed with,
        "color": anything that can be used to construct a ManimColor object; usually a [r,g,b,a] float tuple
        }
        if there is no (action["src"],action["dst"]) edge in the graph, an exception will be thrown.

        {
        "type": "vertexcolor",
        "vertex": the key of a vertex from the networkx graph the object was constructed with,
        "color": anything that can be used to construct a ManimColor object; usually a [r,g,b,a] float tuple
        }
        if there is no action["vertex"] vertex in the graph, an exception will be thrown.


        TODO: should detect malformed dictionaries and throw exception if malformed
        '''
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
        AnimatedObject.animate(self, action)

    
    
        
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
          
        
        
        
        

