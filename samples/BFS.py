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
        vertexColor = [1., 0., 1., 0.6]; 
       
        # Do a BFS traversal of the graph

		# duplicate graph
        bfsGraph = nx.Graph() 
        bfsGraph.add_nodes_from([v for v in sceneNXGraph.nodes])
        #bfsGraph.add_weighted_edges_from(weightedEdgesArr)

        # run bfs traversal on graph, using first node as source
        src = list(bfsGraph.nodes)[0];

        # get the edges using NetworkX's algoritm for BFS traversal
        bfs = nx.bfs_edges(bfsGraph, src)

        #put into a list
        bfs_edges = list(bfs)

        # build the animation
        animation_steps = []

        # highlight the source node node
        mark = {}
        animatedgraph.color_vertex(src, srcColor)
        tts.say(f"Starting BFS traversal at source vertex {src}")
        mark[src] = True;
        ma.step()

        # traverse through the edges, marking the edges and vertices
        for edge in bfs_edges:
            src = edge[0]
            dst = edge[1]
                
            # color the edge
            animatedgraph.color_edge(src, dst, edgeColor)
            tts.say(f"Traversing through edge ({src}, {dst})")
            ma.step()
                
            # mark and color the destination vertex
            vertex = dst
            if vertex not in mark:
                mark[vertex] = True
        
                animatedgraph.color_vertex(vertex, vertexColor)
                tts.say(f"Visiting vertex {vertex}")
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

    
