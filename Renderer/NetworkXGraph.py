from AnimatedObject import AnimatedObject
from manim import *
import networkx as nx
from networkx.algorithms import tree



class NetworkXGraph(AnimatedObject):
    sceneNXGraph = None
    sceneGraph = None

    edgeLabels = None #label VGroup
    edgeLabelsObjects = None # a map of vertices to the label object
    
    vertexPositions = None #a map of vertices to 3d coordinate

    vertexLabels = None #label VGroup
    vertexLabelsObjects = None # a map of vertices to the label object

    def _edgeLabelLocation(self, u, v):
        return [ (self.vertexPositions[u][i] + self.vertexPositions[v][i]) / 2.  for i in range (3)]        

   
    def __init__ (self, renderer, data):
        '''
        data is a dict representation of a networkx graph as exported by networkx.node_link_data

        This assumes that each vertex has a "pos" attribute which is a 3d tuple

        This assumes that each vertex has a "weight" attribute to be used as an edge label

        TODO:weight should probably be optional?
        '''
        AnimatedObject.__init__(self, renderer)
        self.sceneNXGraph = nx.node_link_graph(data)

        self.vertexPositions = {v: self.sceneNXGraph.nodes[v]["pos"] for v in self.sceneNXGraph}
        
        self.sceneGraph = Graph.from_networkx(self.sceneNXGraph, 
                                         layout = self.vertexPositions, 
                                         labels = False, #managing labels manually
                                         layout_scale = 4.0,
                                         vertex_config = {"radius": 0.3, "color": BLUE})

        self.vertexLabels = VGroup()
        self.vertexLabelsObjects  = {}
        for v in self.sceneNXGraph:
            label = Text(str(v)).scale(0.75)
            center = self.vertexPositions[v]
            label.move_to(center)
            self.vertexLabels.add(label)
            self.vertexLabelsObjects[v] = label
        
        
        #Weight population
        weightedEdgesArr = [(edge[0], edge[1], self.sceneNXGraph.edges[edge]["weight"]) for edge in self.sceneNXGraph.edges()]

        
        #Weight label mobject creation & positioning.
        self.edgeLabelsObjects = {}
        self.edgeLabels = VGroup()
        for wEdge in weightedEdgesArr:
            edge = (wEdge[0],wEdge[1])
            weight = wEdge[2]
            edgeLine = self.sceneGraph.edges[edge]
            label = Text(str(weight)).scale(0.75)
            center = edgeLine.get_center()
            label.move_to(center)
            self.edgeLabels.add(label)
            self.edgeLabelsObjects[edge] = label
            
        self.renderer.add(self.sceneGraph, self.edgeLabels, self.vertexLabels)

    def _animate_edgecolor(self, action:dict) -> list[Animation]:
        '''
        here is what action should look like
        {
        "type": "edgecolor",
        "src": the key of a vertex from the networkx graph the object was constructed with,
        "dst": the key of a vertex from the networkx graph the object was constructed with,
        "color": anything that can be used to construct a ManimColor object; usually a [r,g,b,a] float tuple
        }
        if there is no (action["src"],action["dst"]) edge in the graph, an exception will be thrown.

        '''
        edge=None
        try:
            temp = (action["src"], action["dst"])
            edge = self.sceneGraph.edges[temp]
        except KeyError as e: #this is normal in undirected graph
            temp = (action["dst"], action["src"])
            edge = self.sceneGraph.edges[temp]
            
        return [ edge.animate.set_color(ManimColor(action["color"])) ]

    def _animate_vertexcolor(self, action:dict) -> list[Animation]:
        '''
        Here is what action should look like
        {
        "type": "vertexcolor",
        "vertex": the key of a vertex from the networkx graph the object was constructed with,
        "color": anything that can be used to construct a ManimColor object; usually a [r,g,b,a] float tuple
        }
        if there is no action["vertex"] vertex in the graph, an exception will be thrown.

        '''
        return [ self.sceneGraph.vertices[action["vertex"]].animate.set_color(ManimColor(action["color"])) ]    

    def _animate_addedge(self, action:dict) -> list[Animation]:
        '''
        Here is what action should look like
        {
        "type": "addedge",
        "src": the key of a vertex from the networkx graph the object was constructed with,
        "dst": the key of a vertex from the networkx graph the object was constructed with,
        "label": optional. But must be a string.
        }
        '''
        src = action["src"]
        dst = action["dst"]
        rets = [ self.sceneGraph.animate.add_edges((src, dst)) ]
        if "label" in action:
            label = Text(str(action["label"])).scale(0.75)
            p = self._edgeLabelLocation(src, dst)
            label.move_to(p)
            self.edgeLabels.add(label)
            rets.append(Create(label))
            self.edgeLabelsObjects[(src,dst)] = label
                
        return rets

    def _animate_setvertexlocation(self, action:dict) -> list[Animation]:
        '''
        Here is what action should look like
        {
        "type": "setvertexlocation",
        "vertex": the key of a vertex from the networkx graph the object was constructed with,
        "pos": a 3d coordinate (list of floats)
        }
        '''
        v = action["vertex"]
        pos = action["pos"] 
        #TODO: check types
        self.vertexPositions[v] = pos
        rets = []
        rets.append(self.sceneGraph.vertices[v].animate.move_to(pos) )
        # shift vertex label if exists
        if v in self.vertexLabelsObjects:
            label = self.vertexLabelsObjects[v]
            rets.append(label.animate.move_to(pos))
        # shift edge label (if exists)
        for e in self.edgeLabelsObjects:
            if e[0] == v or e[1] == v: #not sure we can do better becasue some graph undirected
                edgeLine = self.sceneGraph.edges[e]
                destination = self._edgeLabelLocation(e[0], e[1])
                moveanim = self.edgeLabelsObjects[e].animate.move_to(destination)
                rets.append(moveanim)
                    
        return rets

    def _animate_addvertex(self, action:dict) -> list[Animation]:
        '''
        Here is what action should look like
        {
        "type": "addvertex",
        "vertex": the key for a vertex that should be the networkx compatible and not yet existent
        "pos": optional, a 3d coordinate (list of floats)
        "label": optional, a string
        }
        '''
        rets = []
            
        v = action["vertex"]
        position = {v: [0., 0., .0]}
        if "pos" in action:
            position = {v: action["pos"]}
        self.vertexPositions[v] = position
                
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
            self.vertexLabelsObjects[v] = label

        return rets

    
    def animate(self, action:dict) -> list[Animation]:
        '''
        NetworkXGraph supports a few actions. They are documented in the individual functions.
        
        
        TODO: should detect malformed dictionaries and throw exception if malformed
        '''
        if action["type"] == "edgecolor":
            return self._animate_edgecolor(action)
        
        if action["type"] == "vertexcolor":
            return self._animate_vertexcolor(action)

        if action["type"] == "addedge":
            return self._animate_addedge(action)
            
        if action["type"] == "setvertexlocation":
            return self._animate_setvertexlocation(action)
            
        if action["type"] == "addvertex":
            return self._animate_addvertex(action)
        
        return AnimatedObject.animate(self, action)
