from Animations.AnimatedObject import *
import copy
import networkx as nx

class NetworkXGraph(AnimatedObject):
    '''
    You should not edit the graph past instanciation of the object.
    All modifications to the nx graph should be done through calls to the wrapper object. (this object)
    '''
    nxgraph = None
    nxgraphOrig = None

    def __init__(self, name, nxgraph):
        super().__init__(name)
        self.nxgraph = nxgraph
        self.nxgraphOrig = copy.deepcopy(nxgraph)
    
    def initial(self):
        ret = super().initial()
        ret ["type"] = "nx"
        ret ["data"] = nx.node_link_data((self.nxgraphOrig))
        return ret

    def color_edge(self, src, dst, color):
        stuff = self.base_animation_step()
        stuff["data"] = {"type":"edgecolor",
                         "src":src, "dst":dst,
                         "color":color
                         }
        #TODO: should record in the underlying networkx object?
        #TODO: clone the parameters?
        self.animations.append(stuff)

    def color_vertex(self, vertex, color):
        stuff = self.base_animation_step()
        stuff["data"] = {"type":"vertexcolor",
                         "vertex":vertex, 
                         "color":color
                         }
        #TODO: should record in the underlying networkx object?
        #TODO: clone the parameters?
        self.animations.append(stuff)
        
    def add_edge(self, src, dst):
        stuff = self.base_animation_step()
        #TODO check for existence or exception
        stuff["data"] = {"type":"addedge",
                         "src":src,
                         "dst":dst
                         }
        #TODO: should record in the underlying networkx object?
        #TODO: clone the parameters?
        self.animations.append(stuff)

    def add_vertex(self, vertex, pos=None, label=None):
        '''
        pos is 3d coordinate
        '''
        stuff = self.base_animation_step()
        #TODO check for existence or exception
        stuff["data"] = {"type":"addvertex",
                         "vertex":vertex
                         }
        if pos:
            stuff["data"]["pos"] = pos

        if label:
            stuff["data"]["label"] = label
        
        #TODO: should record in the underlying networkx object?
        #TODO: clone the parameters?
        self.animations.append(stuff)

    def set_vertex_location(self, vertex, pos):
        '''
        pos is 3d coordinate
        '''
        stuff = self.base_animation_step()
        #TODO check for existence or exception
        stuff["data"] = {"type": "setvertexlocation",
                         "vertex": vertex,
                         "pos": pos}
        
        #TODO: should record in the underlying networkx object?
        #TODO: clone the parameters?
        self.animations.append(stuff)
