import sys
from OrderBook import OrderBook
from Order import Order
from random import randint, randrange
from datetime import *

ob = OrderBook()
max_buy, min_sell = 0, 100
for i in range(100):
    order = Order(i, randint(1, 100), randrange(0, 10000, 1), "BUY" if randint(0, 1) == 1 else "SELL", datetime.now() + timedelta(days=randrange(-1000, 1000, 1)))
    if order.side == "BUY" and order.price > max_buy:
        max_buy = order.price
    if order.side == "SELL" and order.price < min_sell:
        min_sell = order.price
    print("test", order)
    ob.process_order(order)
print(ob)
