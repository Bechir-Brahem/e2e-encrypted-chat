import pickle

from server.Helpers import SingletonMeta
from server.services.ChatService import ChatService
from server.services.LoginService import LoginService
from server.services.OnlineUsersService import OnlineUsersService
from server.services.RegisterService import RegisterService


class ActionStrategies(metaclass=SingletonMeta):
    @staticmethod
    def handle(conn, request):
        res=None
        action=''
        if request['action'] == "login":
            res= LoginService.handle(conn, request['payload']).to_bytes(length=4096, byteorder='little')
            action='login'
        elif request['action'] == "register":
            res= RegisterService.handle(conn, request['payload']).to_bytes(length=4096, byteorder='little')
            action='register'
        elif request['action'] == 'online_users':
            res= OnlineUsersService.handle(conn, request['payload'])
            action='online_users'
        elif request['action'] == 'message':
            res= ChatService.handle(conn, request['payload'])
            action='message'
        else:
            raise AttributeError('action unknown')
        return pickle.dumps({'action':action,'payload':res})
