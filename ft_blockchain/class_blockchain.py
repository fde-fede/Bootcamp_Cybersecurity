import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.end_hash = 42
        self.transactions = []

        self.new_block(previous_hash=1, proof=100)
    
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof':proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.chain.append(block)
        self.transactions = []
        return block
    
    def new_transaction(self, sender, recipient, amount):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
            })
        return self.last_block['index'] + 1
    
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof=None):
        proof = last_proof
        self.end_hash=str("42" * (1 + (len(self.chain) // 10)))
        while self.valid_proof(last_proof, proof, self.end_hash) is False:
            proof += 1
        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof, end_hash):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        if (guess_hash[(-1) * (len(end_hash)):] == end_hash):
            print(guess_hash)
        return guess_hash[(-1) * (len(end_hash)):] == end_hash
    
    def register_node(self, address):
        self.nodes.add((urlparse(address)).netloc)

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(last_block)
            print(block)
            if block['previous hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof'], self.end_hash):
                return False
            last_block = block
            current_index += 1
        return True
    
    def solve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.valid_chain(chain):
                    new_chain = chain
                    max_length = length
        if new_chain is not None:
            self.chain = new_chain
            return True
        else:
            return False