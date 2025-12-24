import random
import networkx as nx
from typing import override
from networkx.algorithms import tree
import json
import sys

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
        verticesArr = [i for i in range(vCount)]
        edgesArr = []
        randomEdgeGen(vCount, edgesArr, 2)
        
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


def make_animation(sceneNXGraph):
        weightedEdgesArr = [(edge[0], edge[1], sceneNXGraph.edges[edge]["weight"]) for edge in sceneNXGraph.edges()]

        #Calculate minnimum spanning tree of the graph using Prim's algorithm.
        mstGraph = nx.Graph() #Duplicate graph of sceneNXGraph. Used to calculate minnimum spanning tree.
        mstGraph.add_nodes_from([v for v in sceneNXGraph.nodes])
        mstGraph.add_weighted_edges_from(weightedEdgesArr)
        mst = tree.minimum_spanning_edges(mstGraph, data = True, algorithm="prim")
        mstEdges = list(mst)
        animation_steps = []
        mark = {}
        tts0 = {"applyon":"tts", "data":{"type":"say", "text": f"Marking {mstEdges[0][0]} as initial vertex reached."}}
        mark[mstEdges[0][0]] = True
        animation_steps.append( [ {"applyon":"G", "data": {"type": "vertexcolor", "vertex":mstEdges[0][0], "color":[1.,0.,0.,0.6]} }, tts0] )
        for edge in mstEdges:
                type = "edgecolor"
                if(edge[0], edge[1]) in sceneNXGraph.edges: 
                        temp = (edge[0], edge[1])
                else:
                        temp = (edge[1], edge[0])
                src = temp[0]
                dst = temp[1]
                color = [0.,1.,0.,1.]
                tts1 = {"applyon":"tts", "data":{"type":"say", "text": f"Adding edge ({src}, {dst}) as part of the spanning tree."}}
                animation_steps.append( [ {"applyon": "G", "data": {"type": type, "src": src, "dst":dst, "color": color}} , tts1] )
                
                
                vertex = edge[0]
                if vertex not in mark:
                    type = "vertexcolor"
                    color = [1.,0.,0.,0.6]
                    ahhh = {"applyon":"G", "data": {"type": type, "vertex": vertex, "color": color}}
                    tts2 = {"applyon":"tts", "data":{"type":"say", "text": f"Marking {vertex} as reached."}}
                    mark[vertex] = True
                    animation_steps.append( [ ahhh, tts2] )
                    
                vertex = edge[1]
                if vertex not in mark:
                    type = "vertexcolor"
                    color = [1.,0.,0.,0.6]
                    ahhh = {"applyon":"G", "data": {"type": type, "vertex": vertex, "color": color}}
                    tts2 = {"applyon":"tts", "data":{"type":"say", "text": f"Marking {vertex} as reached."}}
                    mark[vertex] = True
                    animation_steps.append( [ ahhh, tts2] )

        #print (animation_steps)

        return animation_steps


if __name__ == "__main__":
    my_graph = makegraph()
    animation = make_animation(my_graph)

    initial_state = {}
    
    initial_state["G"] = { "type": "nx", "data": nx.node_link_data((my_graph))}
    initial_state["tts"] = {"type": "tts", "data":{}}
    
    data = { "initial": initial_state,
            "animation": animation}

    json_str = json.dumps(data, indent=2)
    with open(sys.argv[1], "w") as out:
        out.write(json_str)

    
