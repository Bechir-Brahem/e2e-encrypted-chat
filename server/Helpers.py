import os
import pickle
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

from cryptography.hazmat.backends import default_backend
from .ServerVars import ServerVars


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


def decrypt_password(password):
    pem_key = open(os.path.join(
        ServerVars.path, 'ca.key'), 'rb').read()
    ca_key = serialization.load_pem_private_key(
        pem_key, password=None, backend=default_backend())
    password = ca_key.decrypt(
        password,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print('[X] Client\'s Password Decrypted')
    return password