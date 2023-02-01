from server.ServerVars import ServerVars

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
import os
class GetCaCertificate:
    @staticmethod
    def handle(*args):
        pem_key = open(os.path.join(ServerVars.path, 'ca.key'), 'rb').read()
        ca_key = serialization.load_pem_private_key(pem_key, password=None, backend=default_backend())
        tmp=ca_key.public_key()
        return tmp.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo)
