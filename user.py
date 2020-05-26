from ecdsa import SigningKey
from scrooge_utils import hash_sha256, hash_object, encoded_hash_object
from transaction import Transaction, CoinCreation
from scrooge_coin import Scroogecoin
import pdb


class User:
    """ A user of the scroogecoin """

    def __init__(self, signing_key=None):
        if signing_key is None:
            self.signing_key = SigningKey.generate()
        else:
            self.signing_key = signing_key
        self.verifying_key = self.signing_key.get_verifying_key()
        self.id = self.get_user_id_from_verifying_key(self.verifying_key)

    def sign(self, message):
        """ Sign a message using the signing key """
        return self.signing_key.sign(message)

    def get_user_id_from_verifying_key(self, verifying_key):
        """ Return the wallet key from the verifying key """
        return hash_object(verifying_key.to_string())

    def verify_signature(self, verifying_key, signature, message):
        """ Verify a signature of a message using the verifying key """
        return verifying_key.verify(signature, message)

    def get_wallet_id_from_verifying_key(self, verifying_key):
        """ Return the wallet key from the verifying key """
        return hash_object(verifying_key.to_string())

    def create_payment(self, payments, blockchain, scrooge):
        """ Transfer coins from this user to other(s).
            Parameters:
             - payments: List of tuples (user id, amount)
             - blockchain: The complete blockchain
             - scrooge: An interface to the Scrooge functions
        """
        consumed_coins = []
        created_coins = []
        my_coins = self.get_coins(blockchain)
        # TODO: Order coins by their values

        for user_id, amount in payments:
            my_coins[:] = [
                coin for coin in my_coins if coin not in consumed_coins
            ]
            for coin in my_coins:
                if coin.value <= amount:
                    consumed_coins.append(coin)
                    consumed_amount = coin.value
                    amount -= coin.value
                else:
                    new_coins = self.devide_coin(coin, amount, scrooge)
                    consumed_ind = self.index_coin_value(new_coins, amount)
                    consumed_coins.append(new_coins[consumed_ind])
                    consumed_amount = amount
                    my_coins.append(new_coins[consumed_ind + 1])
                    amount = 0
                created_coins.append(
                    Scroogecoin(value=consumed_amount, user_id=user_id)
                )
                if amount == 0:
                    break
        return Transaction(created_coins, consumed_coins)

    def index_coin_value(self, coins, value):
        """ Return the index of the first coin with the value
            passed as parameter
        """
        ind = 0
        while ind < len(coins):
            if coins[ind].value == value:
                return ind
            else:
                ind += 1
        return None

    def divide_coin(self, coin, value, scrooge):
        """ Divide a coin in two new coins. The parameter
            'value' is the value of one of the new coins
            and the value of the other is the rest.
            The original coin is consumed and cannot be used
            again.
        """
        if value > coin.value:
            return
        created_coins = [Scroogecoin(value, self.id), Scroogecoin(coin.value - value, self.id)]
        payment = Transaction(created_coins=created_coins, consumed_coins=[coin])
        signature = self.sign(encoded_hash_object(payment))
        new_block = scrooge.process_payment(
            payment, [(self.verifying_key, signature)]
        )
        return new_block.transaction.created_coins

    def get_coins(self, blockchain):
        """ Get all active coins of the blockchain associated
            to this user
        """
        coins = []
        for block in blockchain.blocks:
            tx = block.transaction
            for coin in tx.created_coins:
                if coin.user_id == self.id:
                    coins.append(coin)
            if isinstance(tx, CoinCreation):
                continue
            for coin in tx.consumed_coins:
                if coin.user_id == self.id:
                    coins.remove(coin)
        return coins

    def __str__(self):
        """ String representations of the user """
        separator = '-' * 30 + '\n'
        concat = 'User\n' + separator + \
                 'Id: ' + self.id + '\n' + separator
        return concat
