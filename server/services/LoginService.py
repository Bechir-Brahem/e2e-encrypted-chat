import ldap

from server.ServerVars import ServerVars


class LoginService:
    @staticmethod
    def handle(conn, payload):
        print(payload)
        ldap_conn = ServerVars.ldap_auth_conn
        try:
            # TODO: sanitize user's username
            cn = f"cn={payload['username']},ou=users,ou=system"
            ldap_conn.simple_bind_s(cn, payload['password'])
        except (ldap.INVALID_CREDENTIALS, ldap.UNWILLING_TO_PERFORM):
            print('INVALID CREDENTIALS USER')
            return 1
        print('AUTH SUCCESS')
        ServerVars.sockets[payload['username']]=conn
        return 0
