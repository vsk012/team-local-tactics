import random
from socket import socket
import socket
from _thread import *
import pickle
from game import Game
from network import Network
from socket import SOL_SOCKET, SO_REUSEADDR


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock = socket()
#sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(("localhost", 5550))
s.listen()
print('The server is ready to receive')
conn, _ = s.accept()
winnerstats = conn.recv(1024).decode()
#winnerstats2= conn.recv(1024).decode()
print(winnerstats)
conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock = socket()
#sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(("localhost", 5550))
s.listen()
print('The server is ready to receive')
conn, _ = s.accept()
winnerstats = conn.recv(1024).decode()
#winnerstats2= conn.recv(1024).decode()
print(winnerstats)
conn.close()


with open("serverDatabase.txt","r+") as f:
    f.write(f.read()+winnerstats+"\n")






server = "localhost"
port = 5555

port2 = 5550

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))
except socket.error as e:
    str(e)



s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

rand_numb = random.randint(0,99)
rand_number = str(rand_numb)

##winnerstats = s.recv(4096).decode()
#winnerstats2 = s.recv(4096).decode()
#print(winnerstats)
#print(rand_number +" !!!! this is the random number")





def threaded_client(conn, p, gameId, rand_number):
    global idCount
    
    conn.send(str.encode(str(p)))
    
    rand = str(rand_number)
    conn.send(rand.encode())
    
    

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]
                

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
                    
                    
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()





while True:
    conn, addr = s.accept()
    print("Connected to:", addr)


    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId, rand_number))
    



