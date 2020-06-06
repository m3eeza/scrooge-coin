from ecdsa import SigningKey

from blockchain import Blockchain
from scrooge_utils import hash_sha256, hash_object, encoded_hash_object
from scrooge_coin import Scroogecoin
import pdb

from transaction import CoinCreation


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

    def get_balance(self, blockchain: Blockchain):
        """ Get all active coins of the blockchain associated
            to this User
        """
        blocks = blockchain.blocks + [blockchain.current_block]
        coins = []
        # Check not consumed
        for block in blocks:
            for tx in block.transactions:
                if isinstance(tx, CoinCreation):
                    for coin in tx.created_coins:
                        if coin.user_id == self.id:
                            coins.append(coin)
                else:
                    for coin in tx.coins:
                        if coin.user_id == self.id and tx.receiver.id == self.id:
                            coins.append(coin)
                        if coin.user_id == self.id and tx.sender.id == self.id:
                            coins.remove(coin)
        return coins

    def get_user_id_from_verifying_key(self, verifying_key):
        """ Return the wallet key from the verifying key """
        return hash_object(verifying_key.to_string())

    def verify_signature(self, verifying_key, signature, message):
        """ Verify a signature of a message using the verifying key """
        return verifying_key.verify(signature, message)

    def get_wallet_id_from_verifying_key(self, verifying_key):
        """ Return the wallet key from the verifying key """
        return hash_object(verifying_key.to_string())

    def __str__(self):
        """ String representations of the user """
        separator = '-' * 30 + '\n'
        concat = 'User\n' + separator + \
                 'Id: ' + self.id + '\n' + separator
        return concat
