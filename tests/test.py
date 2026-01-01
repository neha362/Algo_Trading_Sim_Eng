from engine.OrderBook import OrderBook
from engine.Order import Order
from random import randint, randrange
from time import *

ob = OrderBook()
max_buy, min_sell = 0, 100

order_list = []
for i in range(100000):
    order = Order(i, randint(1, 1000), randrange(0, 10000, 1), "BUY" if randint(0, 1) == 1 else "SELL", time_ns())
    if order.side == "BUY" and order.price > max_buy:
        max_buy = order.price
    if order.side == "SELL" and order.price < min_sell:
        min_sell = order.price
    order_list.append(order)
x = time_ns()
for order in order_list:
    ob.process_order(order)
print(f"time elapsed (in nanoseconds): {time_ns() - x}")
