"""
Created on Fri Apr  7 12:11:51 2023

@author: zelimirmaletic
"""

import datetime
import hashlib
import json
import config

class Blockchain:
    """
    Represents a blockchain data structure.
    """

    def __init__(self):
        """
        Initializes a Blockchain object.

        It creates a genesis block - the first block in the chain.
        """
        #Initialize a chain which will contain blocks
        self.chain = [] #a simple list containing blocks
        #Create a genesis block - the first block
        #Previous hash is 0 because this is a genesis block!
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash, land_book=None):
        """
        Creates a new block and adds it to the chain.

        Args:
            proof (int): The proof of work for the block.
            previous_hash (str): The hash of the previous block.
            land_book (optional): The data to be stored in the block.

        Returns:
            dict: The created block.
        """
        #Define block as a dictionary
        block = {'index': len(self.chain) + 1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash,
                 'data': land_book
                 }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        """
        Returns the previous block in the chain.

        Returns:
            dict: The previous block.
        """
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        """
        Performs proof of work to find a new valid proof.

        Args:
            previous_proof (int): The proof of the previous block.

        Returns:
            int: The new valid proof.
        """
        new_proof = 1 #nonce value
        check_proof = False
        while check_proof is False:
            #Problem to be solved (this makes the minig hard)
            #operation has to be non-symetrical!!!
            hash_operation = hashlib.sha256(str(config.BLOCKCHAIN_PROBLEM_OPERATION_LAMBDA(previous_proof, new_proof)).encode()).hexdigest()
            #Check if first 4 characters are zeros
            if hash_operation[:len(config.LEADING_ZEROS)] == config.LEADING_ZEROS:
                check_proof = True
            else:
                new_proof += 1
        #Check proof is now true
        return new_proof
    
    def hash_of_block(self, block):
        """
        Calculates the hash of a block.

        Args:
            block (dict): The block to calculate the hash for.

        Returns:
            str: The hash of the block.
        """
        #Convert a dictionary to string (JSON)
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        """
        Checks if a given chain is valid.

        Args:
            chain (list): The chain to be validated.

        Returns:
            bool: True if the chain is valid, False otherwise.
        """
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            #1 Check the previous hash 
            block = chain[block_index]
            if block['previous_hash'] != self.hash_of_block(previous_block):
                return False
            #2 Check all proofs of work
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(config.BLOCKCHAIN_PROBLEM_OPERATION_LAMBDA(previous_proof, proof)).encode()).hexdigest()
            if hash_operation[:len(config.LEADING_ZEROS)] != config.LEADING_ZEROS:
                return False
            #Update variables
            previous_block = block
            block_index += 1
        return True

    def save_chain_to_file(self, filename):
        """
        Saves the blockchain chain to a file.

        Args:
            filename (str): The name of the file to save the chain to.
        """
        with open(filename, 'w') as file:
            json.dump(self.chain, file)

    def load_chain_from_file(self, filename):
        """
        Loads the blockchain chain from a file.

        Args:
            filename (str): The name of the file to load the chain from.
        """
        with open(filename, 'r') as file:
            self.chain = json.load(file)
