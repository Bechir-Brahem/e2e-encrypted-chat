import asyncio
import pickle
import socket
import sys
from asyncio import AbstractEventLoop

import ldap

from .Helpers import SingletonMeta
from .ServerVars import ServerVars


async def echo(conn: socket, loop: AbstractEventLoop) -> None:
    while True:
        d = await loop.sock_recv(conn, 4096)
        request = pickle.loads(d)
        from server.services.ActionStrategies import ActionStrategies
        result = ActionStrategies.handle(conn, request)
        if result is not None:
            await loop.sock_sendall(conn, result)


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"[x] Got a connection from {address}")
        asyncio.create_task(echo(connection, loop))


class App(metaclass=SingletonMeta):

    async def start(self):

        # connect to the LDAP server
        try:
            ServerVars.ldap_admin_conn = ldap.initialize('ldap://localhost:10389', trace_level=1)
            ServerVars.ldap_auth_conn = ldap.initialize('ldap://localhost:10389', trace_level=1)
        except ldap.SERVER_DOWN:
            print("Can't contact LDAP server")
            exit(4)
        try:
            ServerVars.ldap_admin_conn.simple_bind_s('uid=admin,ou=system', 'admin')
        except ldap.INVALID_CREDENTIALS:
            print("ERROR: INVALID ADMIN CREDENTIALS!")
            sys.exit(3)
        print("[X] Admin Authentication successful")

        # prepare
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setblocking(False)
            s.bind((ServerVars.HOST, ServerVars.PORT))
            s.listen()
            print(f"[*] Listening as {ServerVars.HOST}:{ServerVars.PORT}")
            await listen_for_connection(s, asyncio.get_event_loop())


app = None


async def main():
    global app
    app = App()
    await app.start()


if __name__ == '__main__':
    asyncio.run(main())
