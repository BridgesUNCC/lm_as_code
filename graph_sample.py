import networkx as nx
from typing import override
from networkx.algorithms import tree
import json
import sys
from Animations.NetworkXGraph import * 
from Animations.MasterAnimation import *


def makegraph():
        #smal graph
        vCount = 4
        pos = {
            0:(0,3.5,0),
            1:(-1.5,1.5,0),
            2:(1,1.5,0),
            3:(-1.5,-1.5,0),
            4:(1,-1.5,0),
        }

        verticesArr = [i for i in range(vCount)]
        edgesArr = [(0,1), (1,2), (2,3), (3,4), (4,0)]
        
        #Scene graph creation
        sceneNXGraph = nx.Graph()
        sceneNXGraph.add_nodes_from(verticesArr)
        sceneNXGraph.add_edges_from(edgesArr)

        for v in sceneNXGraph:
                nx.set_node_attributes(sceneNXGraph, {v: {"pos": pos[v]}}) #G[v]["pos"] is a 3d position tuple

        
        for edge in edgesArr:
                w = 1
                nx.set_edge_attributes(sceneNXGraph, {edge: {"weight": w}})
        

        return sceneNXGraph



if __name__ == "__main__":
    my_master_anim = MasterAnimation() #This is the main interface object

    #set up the animation objects we need
    my_graph = makegraph()
    animated_graph = NetworkXGraph("G", my_graph)

    my_master_anim.addAnimatedObject("G", animated_graph)

    #actually build the animation
    animated_graph.color_vertex(2, [1.,0.,0.,1.])
    my_master_anim.step()

    animated_graph.add_vertex(6)
    my_master_anim.step()

    animated_graph.set_vertex_location(6, [2.5, -2.5, 1.])
    my_master_anim.step()
    
    animated_graph.add_vertex(7,[-2.5, 0, 0], "foobar")
    my_master_anim.step()

    animated_graph.set_vertex_location(2, [-2.5, -2.5, 1.])
    my_master_anim.step()

    
    animated_graph.color_edge(2, 3, [1.,0.,0.,1.])
    my_master_anim.step()

    
    animated_graph.add_edge(2, 4)
    my_master_anim.step()
    

    # output
    data = my_master_anim.complete_animation_object()
    
    json_str = json.dumps(data, indent=2)
    with open(sys.argv[1], "w") as out:
        out.write(json_str)

    
