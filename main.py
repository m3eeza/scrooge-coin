from scrooge import Scrooge
from scrooge_coin import Scroogecoin
from scrooge_utils import encoded_hash_object
from transaction import Transaction
from user import User
import random
scrooge = Scrooge()
print(scrooge.user)

users = {}
for i in range(100):
    users[i] = User()
    coins = [Scroogecoin(1, users[i].id) for _ in range(10)]
    scrooge.create_coins(coins)
print(scrooge.ledger)

while True:
    user_a = random.choice(list(users.values()))
    user_b = random.choice(list(users.values()))
    pay_coin = Scroogecoin(value=1, user_id=user_b.id)
    payment = Transaction(created_coins=[pay_coin], consumed_coins=[pay_coin])
    signature = user_a.sign(encoded_hash_object(payment))
    payment_result = scrooge.process_payment(
        payment, [(user_a.verifying_key, signature)]
    )
    print(scrooge.ledger)
