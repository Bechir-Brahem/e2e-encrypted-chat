import pickle
from socket import socket

from server.ServerVars import ServerVars


class ChatService:
    @staticmethod
    def handle(conn, payload):
        print('message recieved')
        print(payload)
        dest_socket: socket = ServerVars.sockets[payload['dest']]
        dest_socket.sendall(pickle.dumps(payload['content']))
