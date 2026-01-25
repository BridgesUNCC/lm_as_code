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

        # generate vertices and edges for the graph
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


def make_animation(animatedgraph: NetworkXGraph, tts: TTSanimation, 
                                       ma: MasterAnimation):
        sceneNXGraph = animatedgraph.nxgraph #treat as read only
        weightedEdgesArr = [(edge[0], edge[1], sceneNXGraph.edges[edge]["weight"]) for edge in sceneNXGraph.edges()]

        srcColor = [1.,0.,0.,0.6]
        edgeColor = [0.,1.,0.,1.]
        #vertexColor = [1., 1., 0., 0.6]; 
        vertexColor = [1., 0., 0., 0.6]; 
       
        #Calculate minimum spanning tree of the graph using Prim's algorithm.
        bfsGraph = nx.Graph() #Duplicate graph of sceneNXGraph. Used to calculate minimum spanning tree.
        bfsGraph.add_nodes_from([v for v in sceneNXGraph.nodes])
        bfsGraph.add_weighted_edges_from(weightedEdgesArr)

        # run bfs traversal on graph, using first node as source
        src = list(bfsGraph.nodes)[0];
        bfs = nx.bfs_edges(bfsGraph, src)
        bfs_edges = list(bfs)
        print(bfs_edges)

        animation_steps = []
        mark = {}
        animatedgraph.color_vertex(src, srcColor)
        tts.say(f"Starting BFS traversal at vertex {src}.")
        mark[src] = True;
        ma.step()

        for edge in bfs_edges:
            print (edge)
        #    if(edge[0], edge[1]) in sceneNXGraph.edges: 
        #        temp = (edge[0], edge[1])
        #    else:
        #        temp = (edge[1], edge[0])
            src = edge[0]
            dst = edge[1]
                
            animatedgraph.color_edge(src, dst, edgeColor)

            # color the edge
            tts.say(f"Traversing through edge ({src}, {dst}) as part of the BFS traversal.")
            ma.step()
                
            # mark and color the destination vertex
            vertex = dst
            if vertex not in mark:
                mark[vertex] = True
        
                animatedgraph.color_vertex(vertex, vertexColor)
                tts.say(f"Visiting vertex {vertex}.")
                ma.step()


if __name__ == "__main__":
    my_master_anim = MasterAnimation() #This is the main interface object

    #set up the animation objects we need
    my_graph = makegraph()
    
    tts = TTSanimation("tts")
    animated_graph = NetworkXGraph("G", my_graph)

    my_master_anim.addAnimatedObject("tts", tts)
    my_master_anim.addAnimatedObject("G", animated_graph)

    #actually build the animation
    make_animation(animated_graph, tts, my_master_anim)
    

    # output
    data = my_master_anim.complete_animation_object()
    
    json_str = json.dumps(data, indent=2)
    with open(sys.argv[1], "w") as out:
        out.write(json_str)

    
