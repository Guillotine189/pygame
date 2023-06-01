
def make(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3]) + "," + str(tup[4]) + "," + str(tup[5]) + "," + str(tup[6]) + "," + str(tup[7]) + "," + str(tup[8]) + "," + str(tup[9])


def read_obs_co(msg):
    message = msg.split(',')
    print(message)
    return int(message[0]), int(message[1]), int(message[2]), int(message[3]), int(message[4]), int(message[5]), int(message[6]), int(message[7]), int(message[8]), int(message[9])


mess = [(1650, 685),(2150, 715),(2650, 728),(3150, 697),(3650, 734),(1650, 130.5),(2150, 46.5),(2650, 98.5),(3150, 66.0),(3650,140.5)]
mess = make(mess)

print(mess)
print()
print()
print()
mess = read_obs_co(mess)
print(mess)
