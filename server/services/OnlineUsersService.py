import pickle

from server.ServerVars import ServerVars


class OnlineUsersService:
    @staticmethod
    def handle(conn, payload):
        return pickle.dumps(list(ServerVars.sockets.keys()))
