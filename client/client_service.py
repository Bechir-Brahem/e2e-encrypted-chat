import logging
import pickle
import socket
import sys
import time
from threading import Thread

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import (Encoding)
from cryptography.x509.oid import NameOID


class ClientService:
    HOST = "localhost"
    PORT = 42069
    dest_username = ""
    src_username = ''

    def __init__(self):
        self.peer_cert = None
        self.cert = None
        self.private_key = None
        self.cbk = None
        connected = False
        counter = 0
        while not connected:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.HOST, self.PORT))
                print('[X] socket bound to server')
                connected = True
            except ConnectionRefusedError as e:

                logging.error("Could not connect to server")
                logging.error("Retrying 1 second...")
                time.sleep(1)
                if counter > 4:
                    logging.error('cannot connect to server')
                    sys.exit(4)
                counter += 1

    def authenticate(self, username, password):
        self.socket.sendall(pickle.dumps({"action": "login", "payload": {"username": username, "password": password}}))

        result = self.socket.recv(4096)

        result = int.from_bytes(result, byteorder='little')
        if (result == 0):
            self.src_username = username
            self.gen_cert()
        return result

    def register(self, username, password):
        self.socket.sendall(
            pickle.dumps({"action": "register", "payload": {"username": username, "password": password}}))

        result = self.socket.recv(4096)
        result = int.from_bytes(result, byteorder='little')
        if (result == 0):
            self.src_username = username
            self.gen_cert()
        return result

    def getOnlineUsers(self):
        self.socket.sendall(pickle.dumps({"action": "online_users", "payload": {}

                                          }))

        result = self.socket.recv(4096)
        result = pickle.loads(result)
        return result

    def setClientDistination(self, dest, src):
        self.dest_username = dest
        self.src_username = src

    def gen_cert(self):
        self.generate_privateK()
        print('[X] Private Key Generated')
        csr = self.generate_csr()
        print('[X] Certificate Request generated')
        self.socket.sendall(pickle.dumps({
            'action': 'sign_csr',
            'payload': {
                'csr': csr,
                'username': self.src_username
            }}))
        print('[X] Certificate Signing Request Sent')
        self.cert = self.socket.recv(4096)

    def request_peer_cert(self):
        self.socket.sendall(pickle.dumps({
            'action': 'req_cert',
            'payload': self.dest_username
        }))

        print('[X] Peer Certificate Request Sent')
        self.peer_cert = self.socket.recv(4096)
        self.peer_cert = x509.load_pem_x509_certificate(self.peer_cert, default_backend())

    def enterChat(self, fn):
        self.request_peer_cert()

        thread = Thread(target=self.listen, args=(fn,))
        thread.start()

    def listen(self, fn):
        while True:
            print('[*] waiting for message')
            cipher = self.socket.recv(4096)
            cipher = pickle.loads(cipher)
            message = self.private_key.decrypt(
                cipher,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            message = bytes.decode(message, encoding='utf-8')
            fn(message)

    def sendMessage(self, message):
        encrypted_message = self.peer_cert.public_key().encrypt(
            bytes(message, 'utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        self.socket.sendall(pickle.dumps(
            {
                'action': 'message',
                'payload': {
                    'dest': self.dest_username,
                    'src': self.src_username,
                    'content': encrypted_message}
            }
        ))
        print('[X] message sent')

    def generate_privateK(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

    def generate_csr(self):
        builder = x509.CertificateSigningRequestBuilder() \
            .subject_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u'USER:bechir'),
            x509.NameAttribute(NameOID.COUNTRY_NAME, u'TN'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Ben Arous'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u'Mourouj')
        ])) \
            .add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True
        )
        request = builder.sign(self.private_key, hashes.SHA256(), default_backend())
        return request.public_bytes(Encoding.PEM)
