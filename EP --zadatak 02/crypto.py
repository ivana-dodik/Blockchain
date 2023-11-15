import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

current_dir = os.path.dirname(os.path.abspath(__file__))

def encrypt_data(data, key_path='public.pem'):
    public_key_path = os.path.join(current_dir, key_path)

    # Load the public key from file
    with open(public_key_path, 'rb') as public_key_file:
        public_key = serialization.load_pem_public_key(
            public_key_file.read(),
            backend=default_backend()
        )

    # Encrypt the message using the public key
    encrypted_data = public_key.encrypt(
        data.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Base64 encode the encrypted data
    encoded_encrypted_data = base64.b64encode(encrypted_data).decode('utf-8')

    return encoded_encrypted_data


def decrypt_data(encoded_encrypted_data, key_path='private.pem'):
    private_key_path = os.path.join(current_dir, key_path)

    # Load the private key from file
    with open(private_key_path, 'rb') as private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(),
            password=None,
            backend=default_backend()
        )

    # Base64 decode the encrypted data
    encrypted_data = base64.b64decode(encoded_encrypted_data)

    # Decrypt the encrypted data using the private key
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Return the decrypted data as a string
    return decrypted_data.decode('utf-8')
