import pickle
import socket
import sys

from .Helpers import SingletonMeta


class ClientService(metaclass=SingletonMeta):
    HOST = "localhost"
    PORT = 42069

    def __init__(self):
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
        result= self.socket.recv(4096)
        result=pickle.loads(result)
        print("online users",result)
        return result
