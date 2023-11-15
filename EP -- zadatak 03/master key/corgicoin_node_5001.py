
from uuid import uuid4

from flask import Flask, jsonify, request

import config
from blockchain import Blockchain

# ======================= FLASK APP ===========================================
# Create a Web App (Flask-based)
app = Flask(__name__)

# Creating an address for node on Port 5000
node_address = str(uuid4()).replace('-', '')

# Create a Blockchain
blockchain = Blockchain(mnemonic_words='topic memory voyage owner oven farm agree profit tobacco ecology gold climb')

# Minig a block


@app.route('/mine-block', methods=['GET'])
def mine_block():
    # Get the previous proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    # Get previous hash
    previous_hash = blockchain.hash_of_block(previous_block)
    # Add new block to the blockchain
    block = blockchain.create_block(proof, previous_hash)
    # Add transactions (the receiver is the miner, an award for mining a block)
    blockchain.add_transaction(
        sender=node_address, receiver=blockchain.get_address(), amount=1)
    # Generate a response as a dictionary
    response = {'message': 'Congratulations! You have just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']
                }
    return jsonify(response), 200

# Getting the full Blockchain


@app.route('/get-chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)
                }
    return jsonify(response), 200

# Checking if the blockchain is valid


@app.route('/is-valid', methods=['GET'])
def is_blockchain_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'The Blockchain is valid!'}
    else:
        response = {'message': 'The Blockchain is not valid!'}
    return jsonify(response), 200


# Adding a new transaction to the Blockchain
@app.route('/add-transaction', methods=['POST'])
def add_transaction():
    # Get the JSON file posted in Postman, or by calling this endpoint
    json = request.get_json()
    # Check all the keys in the received JSON
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'ERROR: Some elements of the transaction JSON are missing!', 400  # Bad Request code
    # Add transaction to the next block,
    index = blockchain.add_transaction(
        json['sender'], json['receiver'], json['amount'])
    response = {'message': f'This transaction will be added to block {index}'}
    return jsonify(response), 201  # Created code

# Decentralize a Blockchain

# Connecting new nodes


@app.route('/connect-node', methods=['POST'])
def connect_node():
    json = request.get_json()
    # Connect a new node
    nodes = json.get('nodes')  # List of addresses
    # Make sure that the list is not empty
    if nodes is None:
        return "ERROR: No node", 400
    # Loop over the nodes and add them one by one
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected.',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201  # Created code

# Replacing the chain by the longest chain if needed


@app.route('/replace-chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The node had different chains, so the chain was replaced by the longest one!',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': ' All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200


@app.route('/get-address', methods=['GET'])
def get_address():
    response = {'address:': blockchain.get_address()}
    return jsonify(response), 200


@app.route('/save-to-file', methods=['POST'])
def save():
    json = request.get_json()
    filename = json['filename']
    blockchain.save_blockchain(filename=filename)
    response = {'message': f'Save to {filename}'}
    return jsonify(response), 202


# Running the app
app.run(host=config.HOST, port=5001)
