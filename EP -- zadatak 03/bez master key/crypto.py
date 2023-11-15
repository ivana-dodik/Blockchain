import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

current_dir = os.path.dirname(os.path.abspath(__file__))


def load_private_key(key_path):
    private_key_path = os.path.join(current_dir, key_path)
    print('aaa')

    # Load the private key from file
    with open(private_key_path, 'rb') as private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(),
            password=None,
            backend=default_backend()
        )

    return private_key


def load_public_key(key_path):
    public_key_path = os.path.join(current_dir, key_path)

    # Load the public key from file
    with open(public_key_path, 'rb') as public_key_file:
        public_key = serialization.load_pem_public_key(
            public_key_file.read(),
            backend=default_backend()
        )

    return public_key
