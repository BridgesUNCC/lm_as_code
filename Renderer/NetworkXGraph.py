from AnimatedObject import AnimatedObject
from manim import *
import networkx as nx
from networkx.algorithms import tree



class NetworkXGraph(AnimatedObject):
    sceneNXGraph = None
    sceneGraph = None
    edgeLabels = None
    vertexLabels = None
    
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
                                         labels = False, #managing labels manually
                                         layout_scale = 4.0,
                                         vertex_config = {"radius": 0.3, "color": BLUE},
                                         edge_type = DashedLine)

        self.vertexLabels = VGroup()
        for v in self.sceneNXGraph:
            label = Text(str(v)).scale(0.75)
            center = the_pos[v]
            label.move_to(center)
            self.vertexLabels.add(label)
        
        
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
            
        self.renderer.add(self.sceneGraph, self.edgeLabels, self.vertexLabels)

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

        if action["type"] == "vertexcolor":
            return [ self.sceneGraph.vertices[action["vertex"]].animate.set_color(ManimColor(action["color"])) ]

        if action["type"] == "addedge":
            src = action["src"]
            dst = action["dst"]
            return [ self.sceneGraph.animate.add_edges((src, dst)) ]

        if action["type"] == "setvertexlocation":
            v = action["vertex"]
            pos = action["pos"] # TODO: needs to shift the label too (vertex and edge)
            return [ self.sceneGraph.vertices[v].animate.move_to(pos) ]

        if action["type"] == "addvertex":
            rets = []
            
            v = action["vertex"]
            position = None
            if "pos" in action:
                position = {v: action["pos"]}

            rets.append(self.sceneGraph.animate.add_vertices(v, positions=position))
                
            if "label" in action: 
                #position?
                label = Text(str(v)).scale(0.75)
                center = [0,0,0]
                if "pos" in action:
                    center = action["pos"]
                label.move_to(center)
                self.vertexLabels.add(label)
                rets.append(Create(label))

            return rets
        

        
        return AnimatedObject.animate(self, action)
