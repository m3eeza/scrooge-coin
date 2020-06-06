from blockchain import Blockchain
from block import Block
from ecdsa import SigningKey
from transaction import CoinCreation, Transaction
from scrooge_utils import hash_sha256, hash_object, encoded_hash_object
from scrooge_coin import Scroogecoin, CoinId
from user import User


class Scrooge:
    """ Trusted entity that creates and manages the blockchain """

    def __init__(self):
        self.user = User()
        self.ledger = Blockchain()

    def create_coins(self, coins):
        """ Add a CoinCreation transaction to the blockchain
            creating the coins passed as parameters. Return
            the hash of the added block.
        """
        transaction = CoinCreation(created_coins=coins)
        return self.ledger.add_transaction(transaction)

    def process_payment(self, payment):
        """ Process a payment sent by a user.
            The parameter signatures is a list of tuples with
            the users' validation keys as the first component
            and the payment signatures as the second component.
        """
        # Verify users' signatures
        if not self.verify_signature(payment):
            return 'Invalid Transaction: Invalid signature'

        # verify that the sender has enough coins to transfer
        if not len(payment.coins) == payment.amount:
            return 'Invalid Transaction: Sender does not possess enough coins'

        # Check if all the coins that are being transferred
        # exist and were not consumed previously
        if not self.ledger.check_coins(payment.coins):
            return 'Invalid Transaction: Attempt Double Spending detected'
        self.ledger.add_transaction(payment)
        return 'ACCEPTED TRANSACTION'

    def verify_signature(self, transaction: Transaction):
        """ Verify a list of transaction signatures """
        # Verify all signatures with their corresponding
        # public keys

        return self.user.verify_signature(transaction.sender.verifying_key,
                                          transaction.signature, encoded_hash_object(transaction))
