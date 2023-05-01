import hashlib
import json
from flask import Flask, jsonify, request
from uuid import uuid4
from time import time
from POS_class import Blockchain

app = Flask(__name__)

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    if not all(item in values for item in ['sender', 'recipient', 'amount', 'balance']):
        return 'Missing values', 400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'], values['balance'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    selected=(blockchain.proof_of_stake())
    blockchain.new_transaction(
        sender="0",
        recipient=selected.address,
        amount=42,
        balance=selected.balance
    )
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'timestamp': block['timestamp'],
        'transactions': block['transactions'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/chain', methods = ['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length':len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    for node in nodes:
        blockchain.register_node(node)
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.solve_conflicts()
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is still valid',
            'new_chain': blockchain.chain
        }
    return jsonify(response), 200

if __name__ == '__main__':
    print("INTRODUCE PORT:")
    port_i = int(input())
    print("\nINTRODUCE NUMBER OF ACCOUNTS:")
    number_acc = int(input())
    blockchain = Blockchain(number_acc)
    app.run(host='0.0.0.0', port = port_i)