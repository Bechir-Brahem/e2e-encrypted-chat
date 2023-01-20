import pickle
import socket
import sys
from threading import Thread

from .ChatView import ChatState
from .Helpers import SingletonMeta


class ClientService(metaclass=SingletonMeta):
    HOST = "localhost"
    PORT = 42069
    dest_username = ""
    src_username = ''

    def __init__(self):
        self.cbk = None
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.HOST, self.PORT))
            print('[X] socket bound to server')
        except ConnectionRefusedError as e:
            print('ERROR: cannot connect to server')
            sys.exit(4)

    def authenticate(self, username, password):
        self.socket.sendall(pickle.dumps({
            "action": "login",
            "payload": {
                "username": username,
                "password": password
            }
        }))

        result = self.socket.recv(4096)

        result = int.from_bytes(result, byteorder='little')
        print('result', result)
        return result

    def register(self, username, password):
        self.socket.sendall(pickle.dumps({
            "action": "register",
            "payload": {
                "username": username,
                "password": password
            }
        }))

        result = self.socket.recv(4096)
        result = int.from_bytes(result, byteorder='little')
        print('result:', result)
        return result

    def getOnlineUsers(self):
        self.socket.sendall(pickle.dumps({
            "action": "online_users",
            "payload": {}

        }))

        result = self.socket.recv(4096)
        result = pickle.loads(result)
        print("online users", result)
        return result

    def setClientDistination(self, dest, src):
        ClientService.dest_username = dest
        ClientService.src_username = src

    def enterChat(self, fn):
        thread = Thread(target=self.listen)
        self.cbk = fn
        thread.start()

    def listen(self):
        while True:
            print('waiting for message')
            message = self.socket.recv(4096)
            message = pickle.loads(message)
            print('message received',message)
            self.cbk(message)


    def sendMessage(self, message):
        self.socket.sendall(pickle.dumps({
            'action': 'message',
            'payload': {
                'dest': self.dest_username,
                'src': self.src_username,
                'content': message
            }
        }))
        print('message sent')
