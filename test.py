import sys
from OrderBook import OrderBook
from Order import Order
from random import randint, randrange
from time import *

ob = OrderBook()
max_buy, min_sell = 0, 100
for i in range(100):
    order = Order(i, randint(1, 10000), randrange(0, 10000, 1), "BUY" if randint(0, 1) == 1 else "SELL", time_ns())
    if order.side == "BUY" and order.price > max_buy:
        max_buy = order.price
    if order.side == "SELL" and order.price < min_sell:
        min_sell = order.price
    print("test", order)
    ob.process_order(order)
    sleep(randint(1, 1000)/1000)
print(ob)
