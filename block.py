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

    def is_empty(self):
        return not self.transactions

    def is_full(self):
        return len(self.transactions) == 10

    def __str__(self):
        return f'''Block:  {self.id} 
Hash previous block: {self.hash_previous_block}
{self.transactions}'''
