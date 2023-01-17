from ldap.ldapobject import LDAPObject


class ServerVars:
    HOST = "localhost"
    PORT = 42069
    sockets = {}
    ldap_admin_conn: LDAPObject = None
    ldap_auth_conn: LDAPObject = None
