from manim import *
import random
import networkx as nx
from typing import override
from networkx.algorithms import tree
#from jsons.handlejson import importjson
from Assignment import Assignment

#Helper function used to randomly populate a graph's edges and nodes. 
#Utilized by the SPFAlgorithm Class.
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
        sceneNXGraph = nx.DiGraph() #Ensures edge tuple (u, v) doesn't get flipped to (v, u).
        sceneNXGraph.add_nodes_from(verticesArr)
        sceneNXGraph.add_edges_from(edgesArr)

        for v in sceneNXGraph:
                print (v, pos[v])
                nx.set_node_attributes(sceneNXGraph, {v: {"pos": pos[v]}}) #G[v]["pos"] is a 3d position tuple

        
        for edge in edgesArr:
                w = random.randrange(1,10)
                nx.set_edge_attributes(sceneNXGraph, {edge: {"weight": w}})
        
                
        return sceneNXGraph

                      
#Class used to implement Prim's Shortest Path First Algorithm. No Interactivity.   
class SPFAlgorithm(Scene):
    def construct(self):

        sceneNXGraph = makegraph()

        the_pos = {v: sceneNXGraph.nodes[v]["pos"] for v in sceneNXGraph}
        
        sceneGraph = Graph.from_networkx(sceneNXGraph, 
                                         layout = the_pos, 
                                         labels = True, 
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
        
        #Calculate minnimum spanning tree of the graph using Prim's algorithm.
        mstGraph = nx.Graph() #Duplicate graph of sceneNXGraph. Used to calculate minnimum spanning tree.
        mstGraph.add_nodes_from([v for v in sceneNXGraph.nodes])
        mstGraph.add_weighted_edges_from(weightedEdgesArr)
        mst = tree.minimum_spanning_edges(mstGraph, data = True, algorithm="prim")
        mstEdges = list(mst)
        
        #Animation.
        self.add(sceneGraph, edgeLabels)
        self.play(sceneGraph.vertices[mstEdges[0][0]].animate.set_color(RED)) #Highlights first node.
        for edge in mstEdges:
            #Matching edge values to a tuple in the original edges array (value order inconsistent between sceneGraph & mstGraph)
            if(edge[0], edge[1]) in sceneNXGraph.edges: 
                temp = (edge[0], edge[1])
            else:
                temp = (edge[1], edge[0])
            self.play(sceneGraph.edges[temp].animate.set_color(RED)) #Highlight the chosen edge.
            if sceneGraph.vertices[temp[0]].get_color() != RED: #Check if the first node is highlighted.
                self.play(sceneGraph.vertices[temp[0]].animate.set_color(RED))
            if sceneGraph.vertices[temp[1]].get_color() != RED: #Check if the second node is highlighted
                self.play(sceneGraph.vertices[temp[1]].animate.set_color(RED))
            
        
        
            
            
        
            
        
        
        
        
        

