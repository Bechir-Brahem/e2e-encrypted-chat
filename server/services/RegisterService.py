import ldap
from ldap import modlist
from server.Helpers import decrypt_password

from server.ServerVars import ServerVars


class RegisterService:
    @staticmethod
    def handle(conn, payload):
        print(payload)
        ldap_conn = ServerVars.ldap_admin_conn
        # result = ldap_conn.search_s(cn, payload['password'])
        password = decrypt_password(payload['password'])


        dn = f"cn={payload['username']},ou=users,ou=system"
        attrs = {
            'objectclass': [b'person', b'top'],
            'cn': bytes(payload['username'], 'utf-8'),
            'sn': bytes(payload['username'], 'utf-8'),
            'userPassword': password
        }

        # Convert our dict to nice syntax for the add-function using modlist-module
        ldif = modlist.addModlist(attrs)

        # Do the actual synchronous add-operation to the ldapserver
        try:
            ldap_conn.add_s(dn, ldif)
        except ldap.ALREADY_EXISTS:
            print(2)
            return 2
        except ldap.LDAPError:
            print(1)
            return 1
        print('REGISTER SUCCESS')
        ServerVars.sockets[payload['username']]=conn
        return 0
