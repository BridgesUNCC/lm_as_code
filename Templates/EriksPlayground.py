from manim import *
import random
import networkx as nx
from typing import override
from networkx.algorithms import tree
import json

#Helper function used to randomly populate a graph's edges and nodes. 
def randomEdgeGen(vCount: int, edgesArr: list):
    for i in range(vCount):
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
            0:(0,4,0),
            1:(-1.5,1.5,0),
            2:(1,1.5,0),
            3:(-1.5,-1.5,0),
            4:(1,-1.5,0),
            5:(0,-4,0),
            6:(-4,0,0),
            7:(4,0,0)
        }
        verticesArr = [i for i in range(vCount)]
        edgesArr = []
        randomEdgeGen(vCount, edgesArr)
        
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
        

        jsonserial = nx.node_link_data((sceneNXGraph))
        print (jsonserial)
        
        return jsonserial


def make_animation(sceneNXGraph):
        weightedEdgesArr = [(edge[0], edge[1], sceneNXGraph.edges[edge]["weight"]) for edge in sceneNXGraph.edges()]

        #Calculate minnimum spanning tree of the graph using Prim's algorithm.
        mstGraph = nx.Graph() #Duplicate graph of sceneNXGraph. Used to calculate minnimum spanning tree.
        mstGraph.add_nodes_from([v for v in sceneNXGraph.nodes])
        mstGraph.add_weighted_edges_from(weightedEdgesArr)
        mst = tree.minimum_spanning_edges(mstGraph, data = True, algorithm="prim")
        mstEdges = list(mst)
        animation_steps = []
        animation_steps.append( [ {"type": "vertexcolor", "vertex":mstEdges[0][0], "color":[1.,0.,0.,1.]} ] )
        for edge in mstEdges:
                type = "edgecolor"
                if(edge[0], edge[1]) in sceneNXGraph.edges: 
                        temp = (edge[0], edge[1])
                else:
                        temp = (edge[1], edge[0])
                src = temp[0]
                dst = temp[1]
                color = [0.,1.,0.,1.]
                animation_steps.append( [ {"type": type, "src": src, "dst":dst, "color": color} ] )
                type = "vertexcolor"
                vertex = edge[0]
                color = [1.,0.,0.,1.]
                ahhh = {"type": type, "vertex": vertex, "color": color}
                type = "vertexcolor"
                vertex = edge[1]
                color = [1.,0.,0.,1.]
                bhhh = {"type": type, "vertex": vertex, "color": color}
                animation_steps.append( [ ahhh, bhhh ] )
        #print (animation_steps)
        animation_json = json.dumps(animation_steps)
        print (animation_json)
        return animation_json

class Renderer(Scene):
    def construct(self):

        sceneNXGraph = nx.node_link_graph(makegraph())
        animation_steps = json.loads(make_animation(sceneNXGraph))
        
        the_pos = {v: sceneNXGraph.nodes[v]["pos"] for v in sceneNXGraph}
        
        sceneGraph = Graph.from_networkx(sceneNXGraph, 
                                         layout = the_pos, 
                                         labels = True, #Vertex labels
                                         label_fill_color = BLUE,
                                         layout_scale = 4.0, 
                                         edge_type = DashedLine)
        
        #Weight population
        weightedEdgesArr = [(edge[0], edge[1], sceneNXGraph.edges[edge]["weight"]) for edge in sceneNXGraph.edges()]

        
        #Weight label mobject creation & positioning.
        edgeLabels = VGroup()
        for wEdge in weightedEdgesArr:
            edge = (wEdge[0],wEdge[1])
            weight = wEdge[2]
            edgeLine = sceneGraph.edges[edge]
            label = Text(str(weight)).scale(0.75)
            center = edgeLine.get_center()
            label.move_to(center)
            edgeLabels.add(label)

                
        #Animation.
        self.add(sceneGraph, edgeLabels)

        for animation_step in animation_steps:
            the_actions = []
            for action in animation_step:
                if action["type"] == "edgecolor":
                    edge=None
                    try:
                        temp = (action["src"], action["dst"])
                        edge = sceneGraph.edges[temp]
                    except KeyError as e: #this is normal in undirected graph
                        temp = (action["dst"], action["src"])
                        edge = sceneGraph.edges[temp]
                        
                    the_actions.append(edge.animate.set_color(ManimColor(action["color"])))
                if action["type"] == "vertexcolor":
                    the_actions.append (sceneGraph.vertices[action["vertex"]].animate.set_color(ManimColor(action["color"])))
            self.play (the_actions)
                
            
        
        
            
            
        
            
        
        
        
        
        

