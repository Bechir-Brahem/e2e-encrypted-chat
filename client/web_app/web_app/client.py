import asyncio
import pickle
import socket
import sys

from .Helpers import SingletonMeta


class ClientService(metaclass=SingletonMeta):
    HOST = "localhost"
    PORT = 42069
    dest_username = ""
    src_username = ''
    loop = asyncio.get_event_loop()

    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.HOST, self.PORT))
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setblocking(False)
            self.loop.create_task(self.listen(self.loop))
            print('[X] socket bound to server')
        except ConnectionRefusedError as e:
            print('ERROR: cannot connect to server')
            sys.exit(4)
    async def listen(self,loop):
        while True:
            result = loop.sock_recv(4096)
            result = pickle.dumps(result)
            if result['action']=='login':
                self.handle_auth(result['payload'])
            elif result['action']=='register':
                self.handle_(result['payload'])
            if result['action']=='login':
                self.handle_auth(result['payload'])

    def authenticate(self, username, password):
        await self.loop.sock_sendall(self.socket, pickle.dumps({
            "action": "login",
            "payload": {
                "username": username,
                "password": password
            }
        }))

    def handle_auth(self, payload):
        result = int.from_bytes(payload, byteorder='little')
        print('result', result)
        return result

    def register(self, username, password):
        await self.loop.sock_sendall(self.socket, pickle.dumps({
            "action": "register",
            "payload": {
                "username": username,
                "password": password
            }
        }))

    async def handle_register(self, payload):
        result = int.from_bytes(payload, byteorder='little')
        print('result:', result)
        return result

    def getOnlineUsers(self):
        await self.loop.sock_sendall(self.socket, pickle.dumps({
            "action": "online_users",
            "payload": {}

        }))

    def handle_onlineUsers(self, payload):
        result = pickle.loads(payload)
        print("online users", result)
        return result

    def setClientDistination(self, dest, src):
        ClientService.dest_username = dest
        ClientService.src_username = src

    def sendMessage(self, message):
        await self.loop.sock_sendall(self.socket, pickle.dumps({
            'action': 'message',
            'payload': {
                'dest': self.dest_username,
                'src': self.src_username,
                'content': message
            }
        }))
