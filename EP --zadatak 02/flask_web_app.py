import json

import blockchain
import config
from crypto import encrypt_data, decrypt_data
from flask import Flask, jsonify, request, make_response
from land_book import LandBook

# Create a Web App (Flask-based)
app = Flask(__name__)

# Create a Blockchain
blockchain = blockchain.Blockchain()


@app.route('/add-land-book', methods=['POST'])
def add_land_book():
    data = request.json
    land_book = LandBook(**data)

    proof = blockchain.proof_of_work(blockchain.get_previous_block()['proof'])
    previous_hash = blockchain.hash_of_block(blockchain.get_previous_block())

    if land_book is not None:
        land_book_json = json.dumps(land_book.__json__())

        land_book_encrypted = encrypt_data(land_book_json)

        block = blockchain.create_block(proof=proof,
                                        previous_hash=previous_hash,
                                        land_book=land_book_encrypted)
    else:
        block = blockchain.create_block(
            proof=proof, previous_hash=previous_hash)

    response = {
        'message': 'New land registry added!',
        'block_index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 201

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
    # Generate a response as a dictionary
    response = {'message': 'Congratulations! You have just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']
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

@app.route('/save-to-json', methods=['GET'])
def save_to_json():
    blockchain.save_chain_to_file(filename='blockchain.json')
    return make_response('', 204)


# Running the app
app.run(host=config.HOST, port=config.PORT)
