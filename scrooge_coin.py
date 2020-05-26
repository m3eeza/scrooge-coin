class Scroogecoin:
    """ Each coin has an id, a value that is how many scroogecoins
        it represents, and a user id that is its owner.
        The coin id is assigned by Scrooge when the transaction
        that creates the coin is included in the blockchain.
    """

    def __init__(self, value, user_id, coin_id=None):
        self.value = value
        self.user_id = user_id
        self.id = coin_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        if self.id is not None:
            num = self.id.coin_num
        else:
            num = 'N/A'
        return 'Num: ' + str(num) + ', Value: ' + str(self.value) + \
               ', user id: ' + self.user_id

    def __repr__(self):
        return str(self)


class CoinId:
    """ The id of a coin. It has two properties:
        - transaction_id: the index of the block where the
            transaction is included.
        - coin_num: the index of the coin into the transaction.
    """

    def __init__(self, coin_num, transaction_id=None):
        self.coin_num = coin_num
        self.transaction_id = transaction_id
