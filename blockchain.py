from _ast import List

from block import Block
from scrooge_coin import CoinId
from scrooge_utils import hash_sha256
from transaction import Transaction


class Blockchain:
    """ Blockchain is composed by the blockchain itself
        (represented as an array of blocks), and a series
        of functions to manage it.
    """

    def __init__(self):
        self.blocks: List[Block] = []

    def is_empty(self):
        return not self.blocks

    def add_block(self, block):
        """ Add a block to the blockchain. Return the hash
            of the block.
        """
        if not self.is_empty():
            block.hash_previous_block = hash_sha256(str(self.blocks[-1]).encode('utf-8'))
        else:
            block.hash_previous_block = None
        block.id = len(self.blocks)

        self.blocks.append(block)
        return block

    def add_transaction(self, transaction):
        """ Add a transaction to the blockchain. Return the hash
            of the transaction.
        """
        last_block = self.blocks[-1]

        if not last_block.is_empty():
            transaction.hash_previous_transaction = hash_sha256(str(last_block.transactions[-1]).encode('utf-8'))
        else:
            transaction.hash_previous_transaction = None

        if last_block.is_full():
            last_block = self.add_block(Block())
        transaction.id = len(last_block.transactions)

        for index, _ in enumerate(transaction.created_coins):
            transaction.created_coins[index].id = CoinId(index, transaction.id)

        self.blocks[-1].transactions.append(transaction)

        return transaction

    def check_blockchain(self):
        """ Check the blockchain to find inconsistencies """
        blocks = self.blocks

        # The list must have at least one block (the genesis block)
        if len(blocks) == 0:
            return False

        for ind in range(len(blocks) - 1, 0, -1):
            if blocks[ind].hash_previous_block != hash_sha256(blocks[ind - 1]):
                return False
        return True

    def check_coin(self, coin):
        """ Check if the coin was created and was not consumed """
        creation_id = coin.id.transaction_id

        # Check created
        if coin not in self.blocks[creation_id].transaction.created_coins:
            print('WARNING: Coin creation not found')
            return False

        # Check not consumed
        for ind in range(creation_id + 1, len(self.blocks)):
            transaction = self.blocks[ind].transaction
            if isinstance(transaction, Transaction) and coin in transaction.consumed_coins:
                print('WARNING: Double spent attempt detected')
                return False

        return True

    def check_coins(self, coins):
        """ Check a group of coins. If the check_coin function
            returns false for any of the coins then the result is
            false, otherwise the result is true.
        """
        for coin in coins:
            if not self.check_coin(coin):
                return False
        return True

    def get_hash_last_block(self):
        """ Return the hash of the last block of the
            blockchain. If there are not blocks, return
            None.
        """
        if len(self.blocks) > 0:
            return hash_sha256(self.blocks[-1])
        else:
            return None

    def __str__(self):
        separator = '-' * 30 + '\n'
        concat = 'Blockchain \n' + separator
        for block in self.blocks:
            concat += str(block) + separator
        return concat
