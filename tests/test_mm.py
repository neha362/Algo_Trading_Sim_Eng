from engine.OrderBook import OrderBook
from engine.Order import Order
from engine.MarketMaker import MarketMaker
from random import randint, randrange
from time import *

ob = OrderBook()
mm_list = [MarketMaker(i, ob) for i in range(5)]
for mm in mm_list:
    ob.register_mm(mm)
order_list = []
for i in range(6, 100000):
    qty = randrange(0, 10000, 1)
    side = "BUY" if randint(0, 1) == 1 else "SELL"
    price = randrange(0, 10000, 1)
    firm = randrange(0, 4, 1)
    order_list.append(Order(6, firm, price, qty, side, time_ns()))
for mm in mm_list: 
    order_list.extend(mm.generate_spread())
for order in order_list:
    ob.process_order(order)
