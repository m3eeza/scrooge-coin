from scrooge_coin import CoinId
from scrooge_utils import hash_sha256


class Block:
    """ Node of the blockchain
        Each block in the blockchain should have a block ID, 10 valid transactions, a hash of the
        block, and a hash pointer to the previous block.
    """

    def __init__(self, id=None, hash_previous_block=None):
        self.transactions = []
        self.id = id
        self.hash_previous_block = hash_previous_block
        self.signature = None

    def __contains__(self, item):
        return item in self.transactions

    def is_empty(self):
        return not self.transactions

    def is_full(self):
        return len(self.transactions) == 10

    def __str__(self):
        transactions = '\n'.join([_.__short_str__() for _ in self.transactions])
        return f'Block ID:  {self.id}\nHash previous block: {self.hash_previous_block}\nTransactions:\n{transactions}'

    def __short_str__(self):
        block_hash = hash_sha256(str(self).encode('utf-8'))
        return f'Block ID:  {self.id},Block Hash: {block_hash}, Previous Block Hash: {self.hash_previous_block}'

    def __repr__(self):
        output = 'Block Under Construction\n'
        output += ' '.join([str(transaction.id) for transaction in self.transactions])
        return
