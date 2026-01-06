from engine.OrderBook import OrderBook
from engine.Order import Order
from engine.MarketMaker import MarketMaker
from random import randint, randrange
from time import *
import matplotlib.pyplot as plt
import numpy as np

ob = OrderBook()
curr_values = []
datapts = {}
mm_list = [MarketMaker(i) for i in range(5)]
for mm in mm_list:
    ob.register_mm(mm)
    datapts[mm] = []
order_list = []
for i in range(6, 20):
    qty = randrange(0, 600, 1)
    side = "BUY" if randint(0, 1) == 1 else "SELL"
    price = randrange(0, 100, 1)
    firm = randrange(0, 4, 1)
    order_list.append(Order(i, firm, price, qty, side, time_ns()))
value = 0
for mm in mm_list:
        datapts[mm].append(len(curr_values))
curr_values.append(100)
for order in order_list:
    value = 0
    ob.process_order(order)
    for mm in mm_list:
        value += mm.last_prices[-1]
    curr_values.append(value/len(mm_list))
for mm in mm_list:
    print(f"market id: {mm.firm_id}, cash: {mm.cash}, p&l: {mm.pnl}, inventory: {mm.inventory}")
plt.plot(curr_values, label="current average traded values")
for mm in mm_list:
    plt.plot(mm.last_prices, label=f"firm {mm.firm_id} P&L")
plt.legend(loc="upper left")
plt.show()

