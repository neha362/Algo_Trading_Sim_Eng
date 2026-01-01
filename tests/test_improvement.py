import sys
from engine.OrderBook import OrderBook
from engine.Order import Order
from random import randint, randrange
from time import *

sell_order = Order(0, 100, 50, 'SELL', time_ns())
buy_order = Order(0, 105, 50, 'BUY', time_ns())
ob = OrderBook()
ob.process_order(sell_order)
ob.process_order(buy_order)
assert len(ob.asks) == 0 and len(ob.bids) == 0
