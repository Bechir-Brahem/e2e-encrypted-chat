import ldap
from server.Helpers import decrypt_password

from server.ServerVars import ServerVars
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.backends import default_backend
import os


class LoginService:
    @staticmethod
    def handle(conn, payload):
        print(payload)
        ldap_conn = ServerVars.ldap_auth_conn
        try:
            # TODO: sanitize user's username
            password = decrypt_password(payload['password'])
            cn = f"cn={payload['username']},ou=users,ou=system"
            ldap_conn.simple_bind_s(cn, password)
        except (ldap.INVALID_CREDENTIALS, ldap.UNWILLING_TO_PERFORM):
            print('INVALID CREDENTIALS USER')
            return 1
        print('AUTH SUCCESS')
        ServerVars.sockets[payload['username']] = conn
        return 0
