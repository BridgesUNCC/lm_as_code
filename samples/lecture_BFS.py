import random
import networkx as nx
from typing import override
from networkx.algorithms import tree
import json
import sys
from Animations.TTSanimation import *
from Animations.NetworkXGraph import * 
from Animations.MasterAnimation import *
from Animations.Image import *


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
        bfsGraph = sceneNXGraph
        weightedEdgesArr = [(edge[0], edge[1], sceneNXGraph.edges[edge]["weight"]) for edge in sceneNXGraph.edges()]

        srcColor = [1.,0.,0.,0.6]
        edgeColor = [0.,1.,0.,1.]
        vertexColor = [1., 0., 1., 0.6]; 
       
        # Do a BFS traversal of the graph

        # run bfs traversal on graph, using first node as source
        src = list(bfsGraph.nodes)[0];

        bfsOrder=[]
        toVisit=[]
        
        # highlight the source node node
        mark = {}
        animatedgraph.color_vertex(src, srcColor)
        tts.say(f"Starting BFS traversal at source vertex {src}")
        mark[src] = True;
        bfsOrder.append(src)
        toVisit.append(src)
        ma.step()

        
        while len(toVisit) > 0:
            current = toVisit[0]
            toVisit = toVisit[1:] #effectively pop
            print (f"processing {current}")
            tts.say(f"Considering neighbors of vertex {current}")

            ma.step()
            
            for nei in bfsGraph.neighbors(current):
                print (f"neighbor {nei}")
                tts.say(f"Considering edge ({current}, {nei})")
                
                ma.step()
                
                if nei not in mark:
                    mark[nei] = True
        
                    animatedgraph.color_vertex(nei, vertexColor)
                    tts.say(f"Visiting vertex {nei} for the first time")
                    bfsOrder.append(nei)
                    toVisit.append(nei)
                    ma.step()
                else:
                    tts.say(f"Vertex {nei} has already been visited")
                    ma.step()
                    


if __name__ == "__main__":
    my_master_anim = MasterAnimation() #This is the main interface object

    #set up the animation objects we need
    my_graph = makegraph()
    
    slide = Image("slide", "samples/img1.png")
    tts = TTSanimation("tts")
    animated_graph = NetworkXGraph("G", my_graph)
    animated_graph.init_hidecamera()
    
    my_master_anim.addAnimatedObject("slide", slide)
    my_master_anim.addAnimatedObject("tts", tts)
    my_master_anim.addAnimatedObject("G", animated_graph)


    tts.say("Some insightful description of bfs")
    
    my_master_anim.step()
    
    animated_graph.show_camera()
    slide.hide_camera()
    tts.say("Let's look at an example")
    my_master_anim.step()
    
    #actually build the BFS animation
    make_animation(animated_graph, tts, my_master_anim)
    
    animated_graph.hide_camera()
    slide.show_camera()
    tts.say("Wow, you so good at BFS now!")

    my_master_anim.step()
    
    # output
    data = my_master_anim.complete_animation_object()
    
    json_str = json.dumps(data, indent=2)
    with open(sys.argv[1], "w") as out:
        out.write(json_str)

    
