import socket


class Network:
    def __init__(self):
        self.host = '10.0.0.238'
        self.port = 9988
        self.format = 'utf-8'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.first_message = self.connect()


    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            message = self.client.recv(1024).decode(self.format)
            return message
        except Exception as e:
            print(e)

    def send(self, message):
        try:
            self.client.send(message.encode(self.format))
            message = self.client.recv(2048).decode(self.format)
            return message
        except Exception as e:
            print(e)
