from server.Helpers import SingletonMeta
from .ChatService import ChatService
from .LoginService import LoginService
from .OnlineUsersService import OnlineUsersService
from .RegisterService import RegisterService
from .SignCSRService import SignCSRService
from ..ServerVars import ServerVars


class ActionStrategies(metaclass=SingletonMeta):
    @staticmethod
    def handle(conn, request):
        if request['action'] == "login":
            return LoginService.handle(conn, request['payload']).to_bytes(length=4096, byteorder='little')
        elif request['action'] == "register":
            return RegisterService.handle(conn, request['payload']).to_bytes(length=4096, byteorder='little')
        elif request['action'] == 'online_users':
            return OnlineUsersService.handle(conn, request['payload'])
        elif request['action'] == 'sign_csr':
            return SignCSRService.handle(conn,request['payload'])
        elif request['action'] == 'req_cert':
            return ServerVars.certificates[request['payload']]
        elif request['action'] == 'message':
            return ChatService.handle(conn, request['payload'])
        else:
            raise AttributeError('action unknown')
