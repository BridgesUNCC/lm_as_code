import pyglet
from manim import *
import random
from manim.opengl import *
class Assignment():
    locations={}
    last_node=None
    correct_node = None
    incorrect_counter = 0
    incorrect_max = 10
    correct_counter=0
    question_text = None
    feedback_text = None  
    options=[]
    assignments=[]
    total_questions=len(assignments)
    option_text=None
    #grade=correct_node/total_questions
    current_assignment_index=1
    isMultipleChoice=False
    

    #Checks if  answer is correct, plays corresponding animation. If the answer is correct, move to next question
    def check_answer(self,node):
        if self.feedback_text:
            self.remove(self.feedback_text)
            
        if node==self.correct_node:
            
            self.feedback_text=Text("Correct").to_edge(DOWN)
            self.add(self.feedback_text)
            self.is_assignment=False

            self.play(FadeOut(self.feedback_text), FadeOut(self.question_text.scale(0.5)), run_time=0.5 )      
            self.current_assignment_index+=1
            
            self.start_next_assignment()
        else:
            self.incorrect_counter+=1
            if self.incorrect_counter>=self.incorrect_max:
                self.feedback_text = Text("Too many incorrect attempts.").scale(0.25).to_corner(DL)
                self.is_assignment=False
                
            else: self.feedback_text=Text(f"Incorrect ( {self.incorrect_counter}/{self.incorrect_max})").scale(0.25).to_corner(DL)
            self.add(self.feedback_text)

    def start_next_assignment(self):
        if(self.current_assignment_index<len(self.assignments)):
            correct_node,question=self.assignments[self.current_assignment_index]
            self.assignment(correct_node,question,self.all_nodes)
        else:
            self.complete_all_assignments()


    def assignment(self, correct_node, question,all_nodes):
        self.correct_node = correct_node
        self.incorrect_counter = 0
        self.is_assignment = True

        if self.question_text:
            self.remove(self.question_text)
        if self.feedback_text:
            self.remove(self.feedback_text)
        self.question_text = Text(question).to_edge(UP*1.5).scale(0.5)
        self.add(self.question_text)
        self.generate_options(all_nodes)
        
    def complete_all_assignments(self):
        self.clear()
        completion_text=Text("All assignments completed")
        self.add(completion_text)

    def calculate_relative_node_pos(self,nodes,scale):
        camera_center=np.array(self.camera.get_center())
        relative_nodes_pos={}
        for node in self.pos:
            node_pos=np.array(self.pos[node])
            relative_pos=(node_pos-camera_center)/scale
            relative_nodes_pos[node]=relative_pos

        
        return relative_pos
    def generate_options(self,all_nodes):
        possible_correct_options=list(self.correct_node)
        if self.isMultipleChoice:
            if self.options:
                for txt in self.options:
                    self.remove(txt)
            incorrect_nodes = [node for node in all_nodes if node not in self.correct_node]
            assert len(incorrect_nodes)>0
            num_incorrect_needed=max(0,4-len(self.correct_node))
            self.chosen_incorrect = random.sample(incorrect_nodes, min(num_incorrect_needed, len(incorrect_nodes)))
            if len(self.correct_node)>4:
                possible_correct_options=random.sample(self.correct_node, 4)
            
            choices=possible_correct_options+self.chosen_incorrect
            random.shuffle(choices)
            option_labels=["A","B","C","D"]
            self.option_map = {option_labels[i]: choices[i] for i in range(len(choices))}
            
            base_position = LEFT * 5 + UP * 1.5  
            vertical_spacing = 0.75  

            for i, label in enumerate(option_labels):
            
                if i < len(choices):  # Ensure we don't exceed available nodes
                    self.option_text = Text(f"{label}: Node {choices[i]}").scale(0.5).move_to(base_position-UP*(i * vertical_spacing))
                    self.options.append(self.option_text)
                    self.add(self.option_text)
