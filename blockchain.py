from block import Block
from scrooge_coin import CoinId, Scroogecoin
from scrooge_utils import hash_sha256
from transaction import Transaction, CoinCreation



class Blockchain:
    """ Blockchain is composed by the blockchain itself
        (represented as an array of blocks), and a series
        of functions to manage it.
    """

    def __init__(self):
        self.blocks: list[Block] = []
        self.current_block = Block(id=0)

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

        self.blocks.append(block)
        return block

    def add_transaction(self, transaction):
        """ Add a transaction to the blockchain. Return the hash
            of the transaction.
        """

        if not self.current_block.is_empty():
            transaction.hash_previous_transaction = hash_sha256(
                str(self.current_block.transactions[-1]).encode('utf-8'))
        else:
            transaction.hash_previous_transaction = None

        if self.current_block.is_full():
            self.add_block(self.current_block)
            self.current_block = Block(id=len(self.blocks),
                                       hash_previous_block=hash_sha256(str(self.blocks[-1]).encode('utf-8'))
                                       )

        transaction.id = len(self.current_block.transactions)
        if isinstance(transaction, CoinCreation):
            for index, _ in enumerate(transaction.created_coins):
                transaction.created_coins[index].id = CoinId(index, transaction.id, self.current_block.id)
        else:
            for index, _ in enumerate(transaction.coins):
                transaction.coins[index].id = CoinId(index, transaction.id, self.current_block.id)

        self.current_block.transactions.append(transaction)

        return transaction

    def check_blockchain(self):
        """ Check the blockchain to find inconsistencies """
        blocks = self.blocks + [self.current_block]

        # The list must have at least one block (the genesis block)
        if len(blocks) == 0:
            return False

        for ind in range(len(blocks) - 1, 0, -1):
            if blocks[ind].hash_previous_block != hash_sha256(str(blocks[ind - 1]).encode('utf-8')):
                return False
        return True

    def check_coin(self, coin):
        """ Check if the coin was created and was not consumed """
        print(coin)
        block_id, transaction_id = coin.id.block_id, coin.id.transaction_id
        # Check created
        if coin not in self.current_block.transactions[transaction_id].created_coins:
            print('WARNING: Coin creation not found')
            return False

        # Check not consumed
        for ind in range(block_id, len(self.blocks)):
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

    def check_coin(self, coin: Scroogecoin):
        """ Check if the coin was created and was not consumed """
        blocks = self.blocks + [self.current_block]
        block_id, transaction_id = coin.id.block_id, coin.id.transaction_id
        transaction = blocks[block_id].transactions[transaction_id]
        # Check created
        if isinstance(transaction, CoinCreation):
            pass
        elif coin.user_id != transaction.receiver.id:
            print('Invalid Transaction: Coin creation not found!')
            return False

        # Check not consumed
        for block in blocks:
            for tx in block.transactions:
                if not isinstance(tx, CoinCreation) and coin.user_id == tx.sender:
                    for coin in tx.coins:
                        print('Invalid Transaction: Attempt Double Spending detected!')
                        return False
        return True

    def __str__(self):
        separator = '-' * 30 + '\n'
        concat = 'Blockchain: \n' + separator
        blocks = self.blocks + [self.current_block]
        for block in blocks:
            concat += block.__short_str__() + '\n'
        return concat

    def __repr__(self):
        return self.__str__()
