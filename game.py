from cmd import PROMPT
from champlistloader import load_some_champs
#from core import Champion, Match, Shape
import numpy as np
import random
from rich import print
from rich.prompt import Prompt
from rich.table import Table
from network import Network
#from client import tom_liste


champs =[]
rock_percent = [] #[20, 10, 30, 30, 25] format
paper_percent = []
scissor_percent = []

list_for_player2 = []
Ro_Pa_Sc = ["Rock", "Paper", "Scissor"]
random2 = random.randint(0, 99)
random1 = random.randint(0, 99)

with open('some_champs.txt') as f:
            for line in f:
                champ, rock, paper, scissor = line.rstrip().split(',')
                champs.append(champ)
                rock_percent.append(rock)
                paper_percent.append(paper)
                scissor_percent.append(scissor)



class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False 
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True 
        else:
            self.p2Went = True
           

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went
    

    
    def winner(self, random_number):
        winner = -1
        
        player1 = self.moves[0]
        player2 = self.moves[1]
        player1Index = champs.index(str(player1))
        player2Index = champs.index(str(player2))
        
        #generates a list of 100 elements with the probibilities given in some_champs.txt for player1,2
        list_for_player1 = []
        for i in range(int(rock_percent[player1Index])):
            list_for_player1.append("Rock")
        for i in range(int(paper_percent[player1Index])):
            list_for_player1.append("Paper")
        for i in range(int(scissor_percent[player1Index])):
            list_for_player1.append("Scissor")
        
        player1_move = list_for_player1[int(random_number)]
            
        list_for_player2 = []
        for i in range(int(rock_percent[player2Index])):
            list_for_player2.append("Rock")
        for i in range(int(paper_percent[player2Index])):
            list_for_player2.append("Paper")
        for i in range(int(scissor_percent[player2Index])):
            list_for_player2.append("Scissor")
        
        player2_move = list_for_player2[int(random_number)]


 
        if player1_move == "Rock" and player2_move == "Scissor":
            winner = 0
        elif player1_move == "Scissor" and player2_move == "Rock":
            winner = 1
        elif player1_move == "Paper" and player2_move == "Rock":
            winner = 0
        elif player1_move == "Rock" and player2_move == "Paper":
            winner = 1
        elif player1_move == "Scissor" and player2_move == "Paper":
            winner = 0
        elif player1_move == "Paper" and player2_move == "Scissor":
            winner = 1
     
        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
       
        