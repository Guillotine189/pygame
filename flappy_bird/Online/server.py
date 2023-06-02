import socket
import threading
import random

HOST = '10.0.0.238'
PORT = 9900

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

    def get_one_co(self):
        gap = []

        rand5 = random.randint(50, 200)
        rand6 = random.randint(50, 100)
        up_co = 140 + rand5
        down_co = 650 - 3*rand6


        # top = random.randint(100, 215)
        # bottom = random.randint(590, 700)
        gap.append(up_co)
        gap.append(down_co)
        return gap


def read_obs_co(msg):
    message = msg.split(',')
    return float(message[0]), float(message[1])
#
# def read_obs_co(msg):
#     message = msg.split(',')
#     return int(message[0]), int(message[1])

position = [(-100, -100),(-100, -100)]
status = [0, 0]
winner = [0, 0]

def make(tup):
    return str(tup[0]) + "," + str(tup[1])

def DISCONNECT(client, addr):
    clients.remove(client)
    print(f"{addr} DISCONNECTED")




def receive(client, addr, pl_no):
    count = 1
    global running, position, player_no, status, winner
    obs = tube()
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            


            if message == '!D' and player_no == 1:
                player_no = 0
                position = [(-100, -100), (-100, -100)]
                status = [0, 0]
                winner = [0, 0]

            if message == "!D":
                DISCONNECT(client, addr)
                break

            elif message == "OBS_INIT":
                coordinates = obs.get_co()
                for i in range(0, 10):
                    coord = make(coordinates[i])
                    client.send(coord.encode(FORMAT))
                    temp = client.recv(1024).decode(FORMAT)
                    print(f"MSG SENT - {coord}")

            elif message == 'OBS_1':
                coordinate = obs.get_one_co()
                coord = str(coordinate[0])
                client.send(coord.encode(FORMAT))
                client.recv(1024).decode(FORMAT)
                coord = str(coordinate[1])
                client.send(coord.encode(FORMAT))
            #
            # elif message == 'OBS_2':
            #     print("MSG FOR ONE OBS RECV")
            #     coordinate = obs.get_one_co()
            #     print(coordinate)
            #     coord = make(coordinate[1])
            #     client.send(coord.encode(FORMAT))
            #     print(f"MSG SENT 2 {coord}")

            elif message == 'OP':
                client.send('?'.encode(FORMAT))
                req = client.recv(1024).decode(FORMAT)
                req = int(req)
                print(req)
                client.send(f'{req+500}'.encode(FORMAT))
                print(f"OBS CO SENT - {req+ 500}")
            
            
            elif message == 'INIT_POS':
                client.send('?'.encode(FORMAT))
                INITIAL_POS = client.recv(1024).decode(FORMAT)
                INITIAL_POS = read_obs_co(INITIAL_POS)
                client.send("OK".encode(FORMAT))
                if pl_no == 0:
                    position[0] = INITIAL_POS
                else:
                    position[1] = INITIAL_POS

            elif message == 'POSITION?':
                client.send('YOURS?'.encode(FORMAT))
                NEW_POS = client.recv(1024).decode(FORMAT)
                if pl_no == 0:
                    client.send(make(position[1]).encode(FORMAT))
                    position[0] = read_obs_co(NEW_POS)
                else:
                    client.send(make(position[0]).encode(FORMAT))
                    position[1] = read_obs_co(NEW_POS)


            elif message == 'con_stat':
                if count:
                    count -= 1
                if pl_no == 0:
                    status[0] = 1
                    client.send(f'{status[1]}'.encode(FORMAT))
                else:
                    status[1] = 1
                    client.send(f"{status[0]}".encode(FORMAT))


            elif message == 'dead':
                if pl_no == 0:
                    client.send('0'.encode(FORMAT))
                    winner[1] = 1
                else:
                    client.send('0'.encode(FORMAT))
                    winner[0] = 1

            elif message == 'winner?':
                if pl_no == 0 and winner[0]:
                    client.send('1'.encode(FORMAT))
                elif pl_no == 1 and winner[1]:
                    client.send('1'.encode(FORMAT))
                else:
                    client.send('0'.encode(FORMAT))


            elif message == 'RESET':
                player_no = 0
                position = [(-100, -100), (-100, -100)]
                status = [0, 0]
                winner = [0, 0]

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


player_no = 0


while running:
    print("LISTENING...")
    client, addr = server.accept()
    print(f"connected to {addr}")
    if not running:
        print("TURNING OFF SERVER..")
        client.send('0'.encode(FORMAT))
        break
    clients.append(client)
    client.send('200 status - CONNECTED'.encode(FORMAT))

    client_thread = threading.Thread(target=receive, args=(client, addr, player_no))
    client_thread.start()
    player_no += 1