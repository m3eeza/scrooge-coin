class Scroogecoin:
    """ Each coin has an id and a user id that is its owner.
        The coin id is assigned by Scrooge when the transaction
        that creates the coin is included in the blockchain.
    """

    def __init__(self, user_id, coin_id=None):
        self.user_id = user_id
        self.id = coin_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return f'User ID: {self.user_id}, {self.id}'

    def __repr__(self):
        return str(self)


class CoinId:
    """ The id of a coin. It has three properties:
        - block_id: the index of the block where the
            transaction is included.
        - transaction_id: the index of the transaction where the
            coin is included.
        - coin_num: the index of the coin into the transaction.
    """

    def __init__(self, coin_num, transaction_id=None, block_id=None):
        self.coin_num = coin_num
        self.transaction_id = transaction_id
        self.block_id = block_id

    def __str__(self):
        return f'Coin ID: {self.coin_num}, Transaction ID: {self.transaction_id}, Block ID: {self.block_id}'

    def __repr__(self):
        return str(self)
