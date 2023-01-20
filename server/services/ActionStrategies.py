from server.Helpers import SingletonMeta
from server.services.ChatService import ChatService
from server.services.LoginService import LoginService
from server.services.OnlineUsersService import OnlineUsersService
from server.services.RegisterService import RegisterService


class ActionStrategies(metaclass=SingletonMeta):
    @staticmethod
    def handle(conn, request):
        if request['action'] == "login":
            return LoginService.handle(conn, request['payload']).to_bytes(length=4096, byteorder='little')
        elif request['action'] == "register":
            return RegisterService.handle(conn, request['payload']).to_bytes(length=4096, byteorder='little')
        elif request['action'] == 'online_users':
            return OnlineUsersService.handle(conn, request['payload'])
        elif request['action'] == 'message':
            return ChatService.handle(conn, request['payload'])
        else:
            raise AttributeError('action unknown')
