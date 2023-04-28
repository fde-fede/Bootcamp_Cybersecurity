import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse
import random

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.transactions = []
        self.end_hash = 42

        self.new_block(previous_hash=1)
    
    def new_block(self, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.chain.append(block)
        self.transactions = []
        return block
    
    def new_transaction(self, sender, recipient, amount):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1