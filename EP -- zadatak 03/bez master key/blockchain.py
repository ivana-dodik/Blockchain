import datetime
import hashlib
import json
from urllib.parse import urlparse

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

import config
import crypto


class Blockchain:
    def __init__(self, key_path=None):
        # Initialize a chain which will contain blocks
        self.chain = []  # a simple list containing blovks
        # Create a list which contains a list of transactions before they
        # are added to the block. Think of it as a cache of transactions which
        # happened, but are not yet written to a block in a blockchain.
        self.transactions = []
        # Create a genesis block - the first block
        # Previous hash is 0 because this is a genesis block!
        self.create_block(proof=1, previous_hash='0')
        # Create a set of nodes
        self.nodes = set()
        if key_path:
            self.private_key = crypto.load_private_key(key_path)
            self.address = self.generate_address(self.private_key.public_key())

    def create_block(self, proof, previous_hash):
        # Define block as a dictionary
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 # Here we can add any additional data related to the currency
                 'transactions': self.transactions
                 }
        # Now we need to empty the transactions list, since all those transactions
        # are now contained in the block.
        self.transactions = []
        # Append block to the blockchain
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def get_address(self):
        return self.address

    def proof_of_work(self, previous_proof):
        new_proof = 1  # nonce value
        check_proof = False
        while check_proof is False:
            # Problem to be solved (this makes the minig hard)
            # operation has to be non-symetrical!!!
            hash_operation = hashlib.sha256(str(config.BLOCKCHAIN_PROBLEM_OPERATION_LAMBDA(
                previous_proof, new_proof)).encode()).hexdigest()
            # Check if first 4 characters are zeros
            if hash_operation[:len(config.LEADING_ZEROS)] == config.LEADING_ZEROS:
                check_proof = True
            else:
                new_proof += 1
        # Check proof is now true
        return new_proof

    def hash_of_block(self, block):
        # Convert a dictionary to string (JSON)
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            # 1 Check the previous hash
            block = chain[block_index]
            if block['previous_hash'] != self.hash_of_block(previous_block):
                return False
            # 2 Check all proofs of work
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(config.BLOCKCHAIN_PROBLEM_OPERATION_LAMBDA(
                previous_proof, proof)).encode()).hexdigest()
            if hash_operation[:len(config.LEADING_ZEROS)] != config.LEADING_ZEROS:
                return False
            # Update variables
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount, private_key):
        # Create a transaction dictionary
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }

        # Sign the transaction
        signature = private_key.sign(
            json.dumps(transaction, sort_keys=True).encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Add the signature and public key to the transaction
        transaction['signature'] = signature
        transaction['public_key'] = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Add the transaction to the list of transactions
        self.transactions.append(transaction)

        # Return the index of the next block in the blockchain
        previous_block = self.get_previous_block()

        return previous_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        # Add to the list of nodes
        # parsed_url() method returns ParseResult object which has an attribute netloc
        # which is in a format adress:port eg. 127.0.0.1:5000
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            # Find the largest chain (send a request)
            response = requests.get(f'http://{node}/get-chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                # Check chain if it is the longest one and also a valid one
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            # Replace the chain
            self.chain = longest_chain
            return True
        # Otherwise, the chain is not replaced
        return False

    def save_blockchain(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.chain, file, indent=4)

    def load_blockchain(self, filename):
        with open(filename, 'r') as file:
            self.chain = json.load(file)

    def generate_address(self, public_key):
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return hashlib.sha256(public_key_bytes).hexdigest()
