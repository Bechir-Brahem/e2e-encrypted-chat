import os

from ldap.ldapobject import LDAPObject


class ServerVars:
    certificates ={}
    path=os.path.dirname(__file__)
    HOST = "localhost"
    PORT = 42069
    sockets = {}
    ldap_admin_conn: LDAPObject = None
    ldap_auth_conn: LDAPObject = None
