from manim import *
import random
import time
import networkx as nx
from typing import override
from networkx.algorithms import tree
#from jsons.handlejson import importjson
import IPython
import time
from Assignment import Assignment

#Helper function used to randomly populate a graph's edges and nodes.
def graphPopulation(n):
        nodes = [i for i in range(n)]
        edges = []
        #Populating edges array.
        for i in range(n-1):
            if(i+1 >= n):
                continue
            c1 = (i, i+1)
            edges.append(c1)
            if(i+2 >= n):
                continue
            c2 = (i, i+2)
            edges.append(c2)
        #Randomizing the position of nodes.
        pos = {i: (random.randint(-2,2), random.randint(-2,2), 0) for i in range(n)}
        #Creating Labels
        labels = {node: Text(str(node)) for node in nodes}
        #Populating array with all configured graph data to be returned.
        graph_data = [nodes, edges, pos, labels]
        return graph_data


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


#Graph testing class.
class GraphTemp1(MovingCameraScene):
    
    def construct(self):
        n=0 #Node to travel the camera to.
        self.camera.background_color=BLACK
        graph=nx.gnm_random_graph(100,20)  #Generate a random graph from networkX.
        pos=nx.spring_layout(graph) #Set a spring layout on the generated nodes from networkX.
        nodes={i:Dot(point=[pos[i][0]*5,pos[i][1]*5,0],color=WHITE) for i in graph.nodes()}
        edges=[Line(nodes[u].get_center(), nodes[v].get_center(), color=WHITE) for u, v in graph.edges]

        #Scene Population.
        for edge in edges:
            self.add(edge)
        for node in nodes.values():
            self.add(node)
        
        #Move camera to node.
        if n in nodes:
            self.play(self.camera.frame.animate.move_to(nodes[n]))


#Graph testing class.
class GraphTemp2(MovingCameraScene):
    def construct(self):
        start = time.time()
        #Variable n defines number of nodes.
        n = 100
        nodes = [i for i in range(n)]
        edges = []
        #Populating edges array.
        for i in range(n-1):
            if(i+1 >= n):
                continue
            c1 = (i, i+1)
            edges.append(c1)
            if(i+2 >= n):
                continue
            c2 = (i, i+2)
            edges.append(c2)
        #Randomizing the position of nodes.
        pos = {i: (random.randint(-2,2), random.randint(-2,2), 0) for i in range(n)}
        #Creating graph mobject.
        G = Graph(
            nodes, 
            edges, 
            layout = pos,
            layout_config = {"space_x": 10, "space_y": 10},
            layout_scale = 0.25,
            labels = True,
            label_fill_color= 'BLUE'
        )
        
        random_node = random.randint(0, n-1)
        highlight = Circle(radius = 0.25).move_to(pos[random_node]) #Red circle used to highlight nodes. 0.25 is the radius of each node(layout_scale).
        self.add(G)
        self.camera.frame.save_state() #Saves the original position (state) of camera.
        self.play(
            self.camera.frame.animate.set(width = 2).move_to(pos[random_node]), 
            FadeIn(highlight)                        
            )
        self.wait(2)
        self.play(
            FadeOut(highlight),
            Restore(self.camera.frame)
            )
        self.wait(2)
        
        end = time.time()
        print(f"Time taken: {(end-start)*10**3:.03f}ms")        
        
#Class Used to calculate how long graphs of different sizes take to generate within Manim.
class variousSizedGraphs1(Scene):
    def construct(self):
        start = time.time()
        #25 Nodes
        n = 25
        graph_data = graphPopulation(n)
        g_25 = Graph(
            graph_data[0],
            graph_data[1],
            layout = graph_data[2],
            layout_scale = 2
        )
        random_node = random.randint(0, n-1)
        anim_group = [FadeIn(g_25),g_25.vertices[random_node].animate.set_color(RED),Wait(1.5),FadeOut(g_25)]
        self.play(Succession(*anim_group))
        self.remove(g_25,g_25.vertices[random_node])
        end = time.time()
        print(f"25 nodes time taken: {(end-start)*10**3:.03f}ms")        

        #50 nodes
        start = time.time()
        n = 50
        graph_data = graphPopulation(n)
        g_50 = Graph(
            graph_data[0],
            graph_data[1],
            layout = graph_data[2],
            layout_scale = 2
        )
        anim_group = [FadeIn(g_50),g_50.vertices[random_node].animate.set_color(RED),Wait(1.5),FadeOut(g_50)]
        self.play(Succession(*anim_group))
        self.remove(g_50,g_50.vertices[random_node])
        
        end = time.time()
        print(f"50 nodes time taken: {(end-start)*10**3:.03f}ms")  
        
        #100 nodes
        start = time.time()
        n = 100
        graph_data = graphPopulation(n)
        g_100 = Graph(
            graph_data[0],
            graph_data[1],
            layout = graph_data[2],
            layout_scale = 2
        )
        anim_group = [FadeIn(g_100),g_100.vertices[random_node].animate.set_color(RED),Wait(1.5),FadeOut(g_100)]
        self.play(Succession(*anim_group))
        self.remove(g_100,g_100.vertices[random_node])
    
        end = time.time()
        print(f"100 nodes time taken: {(end-start)*10**3:.03f}ms")  
        
        #200 nodes
        start = time.time()
        n = 200
        graph_data = graphPopulation(n)
        g_200 = Graph(
            graph_data[0],
            graph_data[1],
            layout = graph_data[2],
            layout_scale = 2
        )
        anim_group = [FadeIn(g_200),g_200.vertices[random_node].animate.set_color(RED),Wait(1.5),FadeOut(g_200)]
        self.play(Succession(*anim_group))
        self.remove(g_200,g_200.vertices[random_node])
        
        end = time.time()
        print(f"200 nodes time taken: {(end-start)*10**3:.03f}ms")  
        
        
#Class Used to calculate how long graphs of different sizes take to generate within Manim.
#Implements variousSizedGraphs1 but with a while loop.
class variousSizedGraphs2(Scene):
    def construct(self):
        i = 25
        while i <= 200:
            start = time.time()
            graph_data = graphPopulation(i)
            g = Graph(
                graph_data[0],
                graph_data[1],
                layout = graph_data[2],
                layout_scale = 2,
                labels = True
            )
            random_node = random.randint(0, i-1)
            anim_group = [FadeIn(g),g.vertices[random_node].animate.set_color(RED),Wait(1.5),FadeOut(g)]
            self.play(Succession(*anim_group))
            self.remove(g,g.vertices[random_node])
            
            end = time.time()
            print(f"{i} nodes time taken: {(end-start)*10**3:.03f}ms")  
            i = i * 2

#Class used to test the scaling function within Manim.  
class scalingTests(Scene):
    def construct(self):
        graph_data = graphPopulation(10)
        g_10 = Graph(
            graph_data[0],
            graph_data[1],
            layout = graph_data[2], 
            layout_scale = 2.0 
        )
        self.add(g_10)
        self.play(
            ScaleInPlace(g_10, 2.0)
        )


'''
Class used to implement a Breadth First Search Animation. 
Includes full animation and interactivity implementation.
Interactivity is derived from the Assignment.py file.
'''
class BFSAnim(Scene,Assignment):
    def construct(self):
        self.input_mode = 0 #0 = Keyboard, 1 = Mouse
        self.input_lock = False #Locks user input.
        self.all_nodes = []
        self.pos = {}
        self.start_node = 0
        self.option_map = {}
        self.bfs_edges = []
        self.bfs_layers = []
        self.m_graph = None
        self.question_window = None
        Assignment.isMultipleChoice = True
        
        self.build_scene()
        self.fill_assignments()

        Assignment.start_next_assignment(self) 
        
        self.node_radius=0.5
        self.interactive_embed() 
                
    
    #Helper function used to setup the scene at the beginning of each assignment and before any reattempt.
    def build_scene(self):
        self.clear()
        num_nodes = 10
        edge_probability = 0.4
        #Randomly generate networkx graphs until desired graph is found.
        while True:
            nx_graph = nx.erdos_renyi_graph(num_nodes, edge_probability)
            if nx.is_connected(nx_graph):
                break
        node_map = {node: idx for idx, node in enumerate(nx_graph.nodes)} 
        nx_graph = nx.relabel_nodes(nx_graph, node_map)
        
        #Manim graph setup.
        self.m_graph = Graph(list(nx_graph.nodes),
                list(nx_graph.edges),
                layout = "spring",
                layout_scale= 3.8,
                labels = True,
                label_fill_color=WHITE,
                edge_config={"color":BLUE,"stroke_width":2},
                vertex_config = {"fill_opacity": 0, "stroke_color": BLUE, "stroke_width": 2},
                )
        self.question_window = Rectangle(height=8.0,width=4.0).to_edge(LEFT,buff=0.0) #Left hand side question box.
        title = Text("BFS Algorithm").scale(0.4).move_to(self.question_window, UP)
        
        #Add all mobjects to the scene.
        self.add(
            self.question_window,
            self.m_graph.move_to(self.question_window.get_right() + [5,0,0]),
            title,
            Line().put_start_and_end_on(self.question_window.get_left(),self.question_window.get_right()).move_to(title, DOWN)
        )
        
        #populate the pos dict with the positions of each node.
        for i,vertice in enumerate(self.m_graph.vertices.values()):
            self.pos[i] = vertice.get_center().tolist()
        
        self.all_nodes = list(nx_graph.nodes) #Populate a list of all nodes created from the initial networkx graph.
        self.start_node=random.choice(self.all_nodes) #Randomly choose a starting node.
        
        #Use networkX to collect a list/dict of the edges/layers needed to be traversed in a BFS search.
        self.bfs_edges = list(nx.bfs_edges(nx_graph, self.start_node, sort_neighbors=lambda n: sorted(n, reverse=True))) 
        self.bfs_layers = dict(enumerate(nx.bfs_layers(nx_graph, self.start_node)))
        
        self.option_map = {chr(i + 65): node for i, node in enumerate(self.bfs_edges)}

        #Set the starting node to green.
        start_vertex = self.m_graph.vertices[self.start_node]
        self.play(start_vertex.animate.set_color(GREEN), run_time=0.1)
    
    #Populates a list of questions to be presented during the animations.    
    def fill_assignments(self):
        Assignment.assignments = []
        for layer in self.bfs_layers.values():
            #Each question is a tuple containing a list of correct answers and the question.            
            Assignment.assignments.append((layer, "Select which node is next")) 
    
    #Helper function used to highlight the selected node if correct. 
    def highlight_node(self, node):
        edge_to_highlight = None
        for edge in self.bfs_edges:
            if edge[1] == node:
                edge_to_highlight = edge
                self.bfs_edges.remove(edge)
                break
        if edge_to_highlight == None:
            self.play(self.m_graph.vertices[node].animate.set_color(GREEN).set_fill(GREEN,opacity=1.0), run_time = 0.5)
        else:           
            to_node = self.m_graph.vertices[edge_to_highlight[1]]
            if edge_to_highlight not in self.m_graph.edges:
                edge_to_highlight = (edge_to_highlight[1], edge_to_highlight[0])
            self.play(self.m_graph.edges[(edge_to_highlight[0], edge_to_highlight[1])].animate.set_color(GREEN), run_time = 0.5)
            if(to_node.get_color() != GREEN):
                self.play(to_node.animate.set_color(GREEN).set_fill(GREEN, opacity=1.0), run_time = 0.5)
                
    @override
    def assignment(self, correct_node, question, all_nodes):
        self.correct_node = correct_node
        self.incorrect_counter = 0
        self.is_assignment = True
        self.is_end = False

        if self.question_text:
            self.remove(self.question_text)
        if self.feedback_text:
            self.remove(self.feedback_text)
        self.question_text = Text(question).scale(0.65).move_to(self.question_window.get_center() + [0,3,0])
        self.add(self.question_text.scale(0.4))
        if self.input_mode == 0:
            self.generate_options(all_nodes)
    
    @override
    def check_answer(self,node):
        def correct_answer():
            self.feedback_text=Text("Correct",color=GREEN).scale(0.75).move_to(self.question_window, DOWN + [0,0.8,0])
            self.add(self.feedback_text)
            self.highlight_node()
            self.is_assignment=False
            self.play(FadeOut(self.feedback_text), FadeOut(self.question_text), run_time=0.5 )      
            self.current_assignment_index+=1
            self.start_next_assignment()
        if self.feedback_text:
            self.remove(self.feedback_text)
        if node in self.correct_node:
            self.correct_node.remove(node)
            self.feedback_text=Text("Correct",color=GREEN).scale(0.75).move_to(self.question_window, DOWN + [0,0.8,0])
            self.add(self.feedback_text)
            
            self.highlight_node(node)
            
            self.is_assignment=False
            self.play(FadeOut(self.feedback_text), FadeOut(self.question_text), run_time=0.5 )      
            if len(self.correct_node) <= 0:
                Assignment.current_assignment_index += 1
            self.start_next_assignment()
        elif node==self.correct_node:
            correct_answer()
        else:
            self.incorrect_counter+=1
            if self.incorrect_counter>=self.incorrect_max:
                print(self.input_lock)
                self.assignment_end(True)
                self.is_assignment=False
            else:
                self.feedback_text=Text(f"Incorrect ( {self.incorrect_counter}/{self.incorrect_max})", color=RED).scale(0.75).move_to(self.question_window, DOWN).scale(0.5)
                self.add(self.feedback_text)
    
    #Helper function used to clear the scene and prompt the user with an ending screen.  
    @override
    def assignment_end(self, fail: bool):
            self.input_lock = False
            self.is_end = True
            self.clear()
            if(fail):
                completion_text=Text("You failed this assignment").scale(0.75)
            else:
                completion_text=Text("All assignments completed").scale(0.75)
            prompt_box = RoundedRectangle(0.5).set_fill(GREEN_C,1.0)
            self.add(completion_text.move_to([0,1,0]), 
                     prompt_box.move_to([0,-1,0]), 
                     Text("Try again?(Y/N)").move_to(prompt_box.get_center()).scale(0.25)
                     )
            
            
    def on_key_press(self, symbol, modifiers):
        if(self.input_lock or self.input_mode):
            print("Can't type!")
            return
        key = chr(symbol).upper()
        if(self.is_end):
            if(key == 'Y'):
                self.is_end = False
                self.build_scene()
                self.fill_assignments()
                self.is_assignment = True
                Assignment.current_assignment_index = 1
                Assignment.start_next_assignment(self)
            if(key == 'N'):
                pass
        elif key in self.option_map:
            node = self.option_map[key]
            self.input_lock = True
            self.check_answer(node)
            self.input_lock = False
        return super().on_key_press(symbol, modifiers)
    
    def on_mouse_press(self, point, button, modifiers):
            if self.input_lock or not self.input_mode:
                print("Cant click!")
                return
            x,y,z=point
            scene_x=x
            scene_y=y
            
            rounded_x = round(scene_x, 1)
            rounded_y = round(scene_y, 1)
            if rounded_x==-0.0:rounded_x=0.
            if rounded_y == -0.0:rounded_y=0.
            print(rounded_x,rounded_y)
            
            for node, pos in self.pos.items():
                node_x, node_y, _ = pos
                if (abs(scene_x - node_x) <= self.node_radius) and (abs(scene_y - node_y) <= self.node_radius):
                    print(abs(scene_x-node_x))
                    print(abs(scene_y-node_y))
                    
                    self.input_lock = True
                    self.check_answer(node)
                    self.input_lock = False            
            super().on_mouse_press(point, button, modifiers)
                      
#Class used to implement Prim's Shortest Path First Algorithm. No Interactivity.   
class SPFAlgorithm(Scene):
    def construct(self):
        #Scene graph parameters.
        vCount = 8
        pos = {
            0:(0,4,0),
            1:(-2,2,0),
            2:(2,2,0),
            3:(-2,-2,0),
            4:(2,-2,0),
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
        sceneGraph = Graph.from_networkx(sceneNXGraph, 
                                         layout = pos, 
                                         labels = True, 
                                         label_fill_color = BLUE,
                                         layout_scale = 4.0, 
                                         edge_type = DashedLine)
        
        #Weight population
        weights = [random.randrange(1,10) for edge in edgesArr]
        weightedEdgesArr = [(*edge, weights[i]) for i, edge in enumerate(edgesArr)]
        
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
        mstGraph.add_nodes_from(verticesArr)
        mstGraph.add_weighted_edges_from(weightedEdgesArr)
        mst = tree.minimum_spanning_edges(mstGraph, data = True, algorithm="prim")
        mstEdges = list(mst)
        
        #Animation.
        self.add(sceneGraph, edgeLabels)
        self.play(sceneGraph.vertices[mstEdges[0][0]].animate.set_color(RED)) #Highlights first node.
        for edge in mstEdges:
            #Matching edge values to a tuple in the original edges array (value order inconsistent between sceneGraph & mstGraph)
            if(edge[0], edge[1]) in edgesArr: 
                temp = (edge[0], edge[1])
            else:
                temp = (edge[1], edge[0])
            self.play(sceneGraph.edges[temp].animate.set_color(RED)) #Highlight the chosen edge.
            if sceneGraph.vertices[temp[0]].get_color() != RED: #Check if the first node is highlighted.
                self.play(sceneGraph.vertices[temp[0]].animate.set_color(RED))
            if sceneGraph.vertices[temp[1]].get_color() != RED: #Check if the second node is highlighted
                self.play(sceneGraph.vertices[temp[1]].animate.set_color(RED))
            
        
        
            
            
        
            
        
        
        
        
        

