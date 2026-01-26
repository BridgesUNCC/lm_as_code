##This is meant to show two graphs laid out
## This shows location of camera work


import random
import networkx as nx
from typing import override
from networkx.algorithms import tree
import json
import sys
from Animations.TTSanimation import *
from Animations.NetworkXGraph import * 
from Animations.MasterAnimation import *


#Helper function used to randomly populate a graph's edges and nodes. 
def randomEdgeGen(vCount: int, edgesArr: list, degree: int = 1):
    for i in range(vCount):
        for _ in range(degree):
            while(True): #Loop is used to ensure no duplicate edges.
                randEdge = random.randrange(vCount)
                if((randEdge, i) in edgesArr or i == randEdge):
                    continue
                else:
                    break
            edgesArr.append((i, randEdge)) #Add edge tuple to array of edges.        


        
def makegraph():
        #Scene graph parameters.
        vCount = 8
        pos = {
            0:(0,3.5,0),
            1:(-1.5,1.5,0),
            2:(1,1.5,0),
            3:(-1.5,-1.5,0),
            4:(1,-1.5,0),
            5:(0,-3.5,0),
            6:(-3.5,0,0),
            7:(3.5,0,0)
        }

        #smaller graph
        vCount = 4
        pos = {
            0:(0,3.5,0),
            1:(-1.5,1.5,0),
            2:(1,1.5,0),
            3:(-1.5,-1.5,0),
            4:(1,-1.5,0),
        }

        verticesArr = [i for i in range(vCount)]
        edgesArr = []
        randomEdgeGen(vCount, edgesArr, 1)
        
        #Scene graph creation
        sceneNXGraph = nx.Graph()
        sceneNXGraph.add_nodes_from(verticesArr)
        sceneNXGraph.add_edges_from(edgesArr)

        for v in sceneNXGraph:
                #print (v, pos[v])
                nx.set_node_attributes(sceneNXGraph, {v: {"pos": pos[v]}}) #G[v]["pos"] is a 3d position tuple

        
        for edge in edgesArr:
                w = random.randrange(1,10)
                nx.set_edge_attributes(sceneNXGraph, {edge: {"weight": w}})
        

        return sceneNXGraph


if __name__ == "__main__":
    my_master_anim = MasterAnimation() #This is the main interface object

    #set up the animation objects we need
    my_graph = makegraph()
    animated_graph = NetworkXGraph("G", my_graph)
    animated_graph.place_camera([3., -7., -3., 0])

    my_graph2 = makegraph()
    animated_graph2 = NetworkXGraph("G2", my_graph2)
    animated_graph2.place_camera([3., 1., -3., 8.])


    my_master_anim.addAnimatedObject("G", animated_graph)
    my_master_anim.addAnimatedObject("G2", animated_graph2)


    #actually build the animation
    vertexMarkColor = [1.,0.,0.,0.6]  
    animated_graph.color_vertex(0, vertexMarkColor)
    animated_graph2.color_vertex(1, vertexMarkColor)

    my_master_anim.step()

    animated_graph.color_vertex(2, vertexMarkColor)
    animated_graph2.color_vertex(3, vertexMarkColor)

    my_master_anim.step()

    animated_graph2.hide_camera()

    my_master_anim.step()

    animated_graph2.show_camera()

    my_master_anim.step()

    animated_graph2.hide_camera()
    
    animated_graph.move_camera([4., -7., -4., 7])
    
    
    my_master_anim.step()
    
    # output
    data = my_master_anim.complete_animation_object()
    
    json_str = json.dumps(data, indent=2)
    with open(sys.argv[1], "w") as out:
        out.write(json_str)

    
