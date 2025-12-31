import sys
from OrderBook import OrderBook
from Order import Order
from random import randint, randrange
from datetime import *

ob = OrderBook()
for i in range(10):
    order = Order(i, randint(1, 100), .01 * randrange(0, 1000, 1), "BUY" if randint(0, 1) == 1 else "SELL", datetime.now() + timedelta(days=randrange(-1000, 1000, 1)))
    print("test", order)
    ob.add_order(order)
print(ob.asks)
print(ob.bids)
ob.print_book()
