import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.transactions = []
        self.stake_balances = {}

        self.new_block(previous_hash=1, proof=100)
    
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'validator': self.select_validator()
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

    def select_validator(self):
        # Seleccionar el nodo con la mayor cantidad de criptomonedas para ser el validador del siguiente bloque
        validator = max(self.stake_balances, key=self.stake_balances.get)
        return validator

    def validate_transaction(self, sender, recipient, amount):
        # Verificar si el remitente tiene suficientes criptomonedas para enviar
        return self.stake_balances.get(sender, 0) >= amount

    def update_stake_balances(self, sender, recipient, amount):
        # Actualizar los saldos de criptomonedas de los nodos involucrados en la transacción
        self.stake_balances[sender] = self.stake_balances.get(sender, 0) - amount
        self.stake_balances[recipient] = self.stake_balances.get(recipient, 0) + amount

    def register_node(self, address):
        self.nodes.add((urlparse(address)).netloc)

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):
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
    
    def valid_proof(self, last_proof, proof):
        # En POS, la prueba de trabajo no es necesaria, por lo que simplemente se devuelve True
        return True