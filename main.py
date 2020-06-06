import random
import threading

from logger import SafeWriter
from scrooge import Scrooge
from scrooge_coin import Scroogecoin
from scrooge_utils import encoded_hash_object
from transaction import Transaction
from user import User

keep_going = True
LOGGER = SafeWriter("log.txt", "w")


def key_capture_thread():
    global keep_going
    input()
    keep_going = False


scrooge = Scrooge()

users = {}
for i in range(100):
    users[i] = User()
    coins = [Scroogecoin(user_id=users[i].id) for _ in range(10)]
    scrooge.create_coins(coins)

for user in users.values():
    LOGGER.write(f'User ID: {user.id}, balance = {len(user.get_balance(scrooge.ledger))}')

threading.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
while keep_going:
    user_a = random.choice(list(users.values()))
    user_b = random.choice(list(users.values()))
    amount = random.randint(1, 10)
    LOGGER.write(f'Balance: {len(user_a.get_balance(scrooge.ledger))}, {len(user_b.get_balance(scrooge.ledger))}')
    coins = user_a.get_balance(scrooge.ledger)[:amount]
    payment = Transaction(amount=amount, coins=coins, sender=user_a,
                          receiver=user_b)
    payment.signature = user_a.sign(encoded_hash_object(payment))
    payment_status = scrooge.process_payment(
        payment)
    LOGGER.write(f'Balance: {len(user_a.get_balance(scrooge.ledger))}, {len(user_b.get_balance(scrooge.ledger))}')
    LOGGER.write(f'==============={payment_status}================\n')
    LOGGER.write(payment)
    LOGGER.write('+++++++++++++++++++++++++++++++++++++++\n')
    LOGGER.write('================BLOCK UNDER CONSTRUCTION===============\n')
    LOGGER.write(scrooge.ledger.current_block)
    LOGGER.write('+++++++++++++++++++++++++++++++++++++++\n')
    if scrooge.ledger.current_block.is_full() and payment_status == 'ACCEPTED TRANSACTION':
        scrooge.user.sign(encoded_hash_object(scrooge.ledger.current_block))
        LOGGER.write(scrooge.ledger)


LOGGER.write(scrooge.ledger)
LOGGER.close()
print(scrooge.ledger.check_blockchain())
