

class Transaction:
    """ Transfer coins between wallets """

    def __init__(self, amount, coins, sender, receiver):
        self.amount = amount
        self.id = -1
        self.coins = coins
        self.hash_previous_transaction = None
        self.signature = None
        self.sender = sender
        self.receiver = receiver

    def __str__(self):
        return f'Transaction Id: {self.id}, Previous hash: {self.hash_previous_transaction},\n' \
               f'Amount of Coins: {self.amount},\n' \
               f'Sender ID:   {self.sender.id},\n' \
               f'Receiver ID: {self.receiver.id}'

    def __short_str__(self):
        return f'Transaction ID:  {self.id}'

    def __repr__(self):
        return str(self)


class CoinCreation(Transaction):
    """ Creation of coins """

    def __init__(self, created_coins, transaction_id=-1):
        self.created_coins = created_coins
        self.id = transaction_id

    def __str__(self):
        concat = f'''TransID: {str(self.id)} Type: Coin creation\nCreated coins:\n'''
        for coin in self.created_coins:
            concat += str(coin) + '\n'
        return concat

    def __repr__(self):
        return str(self)
