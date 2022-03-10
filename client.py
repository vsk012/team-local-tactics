
import pygame
from champlistloader import load_some_champs
from core import Champion
from network import Network
import pickle
from socket import socket

from rich import print
from rich.prompt import Prompt
from rich.table import Table

#socket = socket()
#server_address = ("localhost", 5555)
#socket.connect(server_address)
#hello = "hello"
#socket.send(hello.encode())
#rand_numb = socket.recv(1024).decode()
#print(rand_numb)
with open("clientDatabase.txt", "r+") as f:
    results = f.read()

sock = socket()
server_address = ("localhost", 5550)
sock.connect(server_address)
sock.send(results.encode())
sock.close()

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")



class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 100
        self.height = 50

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((128,128,128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255,255))
        win.blit(text, (200, 100))

        text = font.render(" Choose Two Champions", 1, (0, 255, 255))
        win.blit(text, (20, 200))
        

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
 
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0,0,0))
 
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
                #text3 = font.render(move3, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In 1", 1, (0, 0, 0))
               
                
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
                #text4 = font.render(move4, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In 1", 1, (0, 0, 0))
          
                
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))
      

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()





btns = [Button("Vain", 50, 450, (0,0,0)),
        Button("Dr. Yi", 300, 450, (0,0,0)),
        Button("Twist", 500, 450, (0,0,0)),
        Button("Guan", 50, 540, (0,0,0)),
        Button("Siva", 300, 540, (0,0,0)),
        Button("Katina", 500, 540, (0,0,0)),
        Button("Asir", 50, 630, (0,0,0)),
        Button("Cactus", 300, 630, (0,0,0)),
        Button("Luanne", 500, 630, (0,0,0)),
        ]



outcome = []

def main():
    
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    random_number_from_server = n.recieve()
    print(random_number_from_server)
    player


    while run:
        
        print(outcome)
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get gameeee")
            with open ("clientDatabase.txt", "w") as f:
                f.write(str(outcome))
            
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break
            
            #outcome = []
            winner = "player "+ str(player+1)+" is winner"
            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner(random_number_from_server) == 1 and player == 1):
                text = font.render("You Won!", 1, (255,0,0))
                winner = "player1 is winner"
            elif(game.winner(random_number_from_server) == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
                winner = "player2 is winner"
            elif game.winner(random_number_from_server) == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
                winner = "tie"
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))
            outcome.append(winner)

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
                pygame.quit()
               

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((180, 180, 180))
        font = pygame.font.SysFont("comicsans", 75)
        text = font.render("Click to Play Game!", 1, (255,0,0))
        text2 = font.render("Welcome to:", 1, (255,0,0))
        font = pygame.font.SysFont("comicsans", 60)
        text3 = font.render("Team Network Tactics!", 1, (255, 215, 0))
        win.blit(text, (10,500))
        win.blit(text2, (10,200))
        win.blit(text3, (10,300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
