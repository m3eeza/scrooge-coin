from blockchain import Blockchain
from block import Block
from ecdsa import SigningKey
from transaction import CoinCreation
from scrooge_utils import hash_sha256, hash_object, encoded_hash_object
from scrooge_coin import Scroogecoin, CoinId
from user import User


class Scrooge:
    """ Trusted entity that creates and manages the blockchain """

    def __init__(self):
        self.user = User()
        self.ledger = Blockchain()
        self.first_block_hash = hash_object(self.add_first_block())
        self.last_block_signature = self.user.sign(
            self.first_block_hash.encode('utf-8')
        )

    def add_first_block(self):
        """ Add the first block to the blockchain and return
            the hash of the genesis block
        """
        first_block = Block()
        return self.ledger.add_block(first_block)

    def create_coins(self, coins):
        """ Add a CoinCreation transaction to the blockchain
            creating the coins passed as parameters. Return
            the hash of the added block.
        """
        transaction = CoinCreation(created_coins=coins)
        return self.ledger.add_transaction(transaction)

    def process_payment(self, payment, signatures):
        """ Process a payment sent by a user.
            The parameter signatures is a list of tuples with
            the users' validation keys as the first component
            and the payment signatures as the second component.
        """
        # Verify users' signatures
        if (not self.verify_signatures(payment, signatures) or
                not payment.verify_balance()):
            return None

        # Check if all the coins that are being transferred
        # exist and were not consumed previously
        if not self.ledger.check_coins(payment.consumed_coins):
            return None

        block = Block(payment)
        return self.ledger.add_block(block)

    def verify_signatures(self, transaction, signatures):
        """ Verify a list of transaction signatures """
        # Verify all signatures with their corresponding
        # public keys
        for verifying_key, signature in signatures:
            if not self.user.verify_signature(verifying_key,
                                              signature, encoded_hash_object(transaction)):
                return False

        # Verify if all users whose coins will be consumed signed
        # the payment
        users = []
        for verifying_key, signature in signatures:
            user_id = self.user.get_user_id_from_verifying_key(verifying_key)
            users.append(user_id)
        for coin in transaction.consumed_coins:
            if coin.user_id not in users:
                return False

        return True
