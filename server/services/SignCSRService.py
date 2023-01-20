import datetime
import os.path
import uuid

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes

from server.ServerVars import ServerVars


class SignCSRService:
    @staticmethod
    def handle(conn, payload):
        username = payload['username']
        csr = x509.load_pem_x509_csr(payload['csr'], default_backend())

        print('aa' ,username)

        pem_cert = open(os.path.join(ServerVars.path, 'ca.crt'), 'rb').read()
        ca = x509.load_pem_x509_certificate(pem_cert, default_backend())
        pem_key = open(os.path.join(ServerVars.path, 'ca.key'), 'rb').read()
        ca_key = serialization.load_pem_private_key(pem_key, password=None, backend=default_backend())

        builder = x509.CertificateBuilder() \
            .subject_name(csr.subject) \
            .issuer_name(ca.subject) \
            .not_valid_before(datetime.datetime.now()) \
            .not_valid_after(datetime.datetime.now() + datetime.timedelta(7)) \
            .public_key(csr.public_key()) \
            .serial_number(int(uuid.uuid4()))
        for ext in csr.extensions:
            builder = builder.add_extension(ext.value, ext.critical)
        certificate = builder.sign(
            private_key=ca_key,
            algorithm=hashes.SHA256(),
            backend=default_backend()
        )
        client_pem_cert = certificate.public_bytes(serialization.Encoding.PEM)
        ServerVars.certificates[username]=client_pem_cert
        print('[X] Client Certificate Signed and Saved')
        return client_pem_cert

