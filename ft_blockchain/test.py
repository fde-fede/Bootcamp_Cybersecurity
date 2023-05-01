import hashlib
import json
from flask import Flask, jsonify, request
from uuid import uuid4
from time import time
from test_class import Blockchain

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    if not all(item in values for item in ['sender', 'recipient', 'amount']):
        return 'Missing values', 400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    blockchain.new_transaction(
        sender="0",
        recipient=
        amount=42,
    )
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(prrof, previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200