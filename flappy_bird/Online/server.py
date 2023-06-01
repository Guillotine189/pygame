import socket
import threading
import random

HOST = '127.0.0.1'
PORT = 9901

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

FORMAT = 'utf-8'

clients = []


# def read(string):
#     string = string.split(',')
#     return int(string[0]), int(string[1])
#
#


running = True



class tube:

    def get_co(self):

        # GET RANDOM COORDINATE FOR Y AXIS
        rand1 = random.randint(100, 200)
        rand2 = random.randint(100, 200)
        rand3 = random.randint(100, 200)
        rand4 = random.randint(100, 200)
        rand5 = random.randint(100, 200)
        rand6 = random.randint(0, 100)
        rand7 = random.randint(0, 100)
        rand8 = random.randint(0, 100)
        rand9 = random.randint(0, 100)
        rand10 = random.randint(0, 100)

        # INITIALIZE OBSTACLE COORDINATE
        # PIPE FACING DOWN CAN COME DOWN MAX = 215 FROM Y AXIS BEFORE IT ENDS
        # PIPE FACING UP CAN COME UP MAX = 590 BELOW Y AXIS BEFORE IT ENDS

        obs1_up_co = (1650, rand1 + 550)
        obs2_up_co = (2150, rand2 + 550)
        obs3_up_co = (2650, rand3 + 550)
        obs4_up_co = (3150, rand4 + 550)
        obs5_up_co = (3650, rand5 + 550)

        obs1_down_co = (1650, rand1 - 1.5 * rand6)
        obs2_down_co = (2150, rand2 - 1.5 * rand7)
        obs3_down_co = (2650, rand3 - 1.5 * rand8)
        obs4_down_co = (3150, rand4 - 1.5 * rand9)
        obs5_down_co = (3650, rand5 - 1.5 * rand10)

        obs_co = []

        obs_co.append(obs1_up_co)
        obs_co.append(obs2_up_co)
        obs_co.append(obs3_up_co)
        obs_co.append(obs4_up_co)
        obs_co.append(obs5_up_co)
        obs_co.append(obs1_down_co)
        obs_co.append(obs2_down_co)
        obs_co.append(obs3_down_co)
        obs_co.append(obs4_down_co)
        obs_co.append(obs5_down_co)

        return obs_co



#
# def read_obs_co(msg):
#     message = msg.split(',')
#     return int(message[0]), int(message[1])




def make(tup):
    return str(tup[0]) + "," + str(tup[1])

def DISCONNECT(client, addr):
    clients.remove(client)
    print(f"{addr} DISCONNECTED")
    # print("LISTENING...")



def receive(client, addr):
    global running
    obs = tube()
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)

            if message == "!D":
                print(message)
                DISCONNECT(client, addr)
                break
            elif message == "OBS_INIT":
                print("MESSAGE FOR OBS RECV")
                coordinates = obs.get_co()
                print(coordinates)
                for i in range(0, 10):
                    coord = make(coordinates[i])
                    client.send(coord.encode(FORMAT))
                    temp = client.recv(1024).decode(FORMAT)
                    print(f"MSG SENT - {coord}")
                print("MSG SENT")


            elif message == 'OP':
                client.send('?'.encode(FORMAT))
                req = client.recv(1024).decode(FORMAT)
                req = int(req)
                print(req)
                client.send(f'{req+500}'.encode(FORMAT))
                print(f"OBS CO SENT - {req+ random.randint(300, 500)}")


            elif message == "!SD":
                print(message)
                print(f"Command to switch off server received {addr}")
                DISCONNECT(client, addr)
                running = False
                break
            else:
                pass
        except:
            print(f"DISCONNECTED FROM {addr}")
            clients.remove(client)
            break


# coordinates = get_co()
# print(coordinates)
# for i in range(9):
#     coord = make(coordinates[i])
#     print(coord)



while running:
    print("LISTENING...")
    client, addr = server.accept()
    print(running)
    print(f"connected to {addr}")
    if not running:
        print("TURNING OFF SERVER..")
        client.send('0'.encode(FORMAT))
        break
    clients.append(client)
    client.send('200 status - CONNECTED'.encode(FORMAT))

    client_thread = threading.Thread(target=receive, args=(client, addr))
    client_thread.start()
