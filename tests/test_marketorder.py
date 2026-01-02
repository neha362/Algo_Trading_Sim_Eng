from engine.OrderBook import OrderBook
from engine.Order import Order
from random import randint, randrange
from time import *

ob = OrderBook()
max_buy, min_sell = 0, 100

order_list = []
for i in range(100):
    qty = randrange(0, 100, 1)
    side = "BUY" if randint(0, 1) == 1 else "SELL"
    if randint(0, 5) > 0:
        order_list.append(Order(i, i, randrange(0, 1000, 1), qty, side, time_ns()))
    else:
        order_list.append(Order(i, i, None, qty, side, time_ns()))
x = time_ns()
for order in order_list:
    ob.process_order(order)
print(f"time elapsed (in nanoseconds): {time_ns() - x}")
