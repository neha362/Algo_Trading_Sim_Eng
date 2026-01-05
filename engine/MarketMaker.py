from time import time_ns
from typing import *
from .Order import Order

type EventType = Literal["FILL", "UPDATE"]


#a market maker class to generate a bid and ask order based on current market orders to generate profit
class MarketMaker:
    #initializer with firm id, order book, and spread_ticks 
    def __init__(self, firm_id, spread_ticks=10, max_pos=500):
        self.inventory = 0
        self.firm_id = firm_id
        self.spread_ticks = spread_ticks
        self.bid = None
        self.ask = None
        self.cash = 0
        self.last_price = 100
        self.pnl = None
        self.max_pos = 500
    
    #generates a spread and returns a bid and ask based on the best possible bid and ask
    def generate_spread(self, orderBook, qty=10):
        best_bid = -orderBook.bids.peekitem()[0] if len(orderBook.bids) > 0 else None
        best_ask = orderBook.asks.peekitem()[0] if len(orderBook.asks) > 0 else None
        adj_value = max(1, int(self.last_price if not best_bid or not best_ask else (best_bid + best_ask)//2 - self.inventory * .1))
        if self.bid != None:
            orderBook.cancel_order(self.bid)
        if self.ask != None:
            orderBook.cancel_order(self.ask)
        self.bid, self.ask = None, None
        if min(qty, self.max_pos - self.inventory) > 0:
            self.bid = Order(time_ns(), self.firm_id, adj_value - self.spread_ticks // 2, qty, "BUY", time_ns())
        if min(qty, self.max_pos + self.inventory) > 0:
            self.ask = Order(time_ns() + 1, self.firm_id, adj_value + self.spread_ticks // 2, qty, "SELL", time_ns())
        return self.bid, self.ask

    #if an order is filled, alter the inventory and the profit accordingly. else, refresh the quotes
    def on_event(self, orderBook, event_type:EventType, qty=None, side=None, initiator_id=None, price=None):
        if event_type == "FILL":
            assert qty != None and side != None
            self.inventory += (qty if side == "BUY" else -qty)
            self.cash -= (qty if side == "BUY" else -qty) * price
            self.pnl = self.inventory * price + self.cash
            self.last_price = price
            self.enter_spread(orderBook)
            return
        if initiator_id == self.firm_id:
            return
        
        self.enter_spread(orderBook, initiator_id=self.firm_id)

    def enter_spread(self, orderBook, initiator_id=None):
        bid, ask = self.generate_spread(orderBook)
        if bid:
            orderBook.process_order(bid, initiator_id=self.firm_id)
        if ask: 
            orderBook.process_order(ask, initiator_id=self.firm_id)

    
    