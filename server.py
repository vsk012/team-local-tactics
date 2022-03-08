from importlib.resources import path
import random
import socket
from _thread import *
import pickle
from game import Game
from pathlib import Path





server = "localhost"
port = 5555

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

                    filename = Path("Database.txt")
                    filename.touch(exist_ok=True)
                    result = conn.recv(4096).decode()
                    with open ("Database.txt", "w+") as f:
                        if result == "1won":
                            f.write(result)
                        if result == "0won":
                            f.write(result)
                        if result == "tie":
                            f.write(result)
                    
                    
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
    



