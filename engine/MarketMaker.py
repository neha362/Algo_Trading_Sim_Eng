from time import time_ns
from typing import *
from .Order import Order

type EventType = Literal["FILL", "UPDATE"]


#a market maker class to generate a bid and ask order based on current market orders to generate profit
class MarketMaker:
    #initializer with firm id, order book, and spread_ticks 
    def __init__(self, firm_id, spread_ticks=10, max_pos=500, ladder_lens=[(5, 1), (10, 2), (20, 5)]):
        self.inventory = 0
        self.firm_id = firm_id
        self.spread_ticks = spread_ticks
        self.bids = []
        self.asks = []
        self.cash = 0
        self.last_prices = [100]
        self.pnl = None
        self.max_pos = 500
        self.ladder_lens = ladder_lens
    
    #generates a spread and returns a bid and ask based on the best possible bid and ask
    def generate_spread(self, orderBook, qty=10):
        adj_values = []
        base = self.last_prices[-1]
        if orderBook.asks and orderBook.bids:
            base = (abs(orderBook.bids.peekitem(0)[0]) + orderBook.asks.peekitem(0)[0])//2
        for tick, count in self.ladder_lens:
            level_val = base - (self.inventory * 0.1)
            for i in range(count):
                adj_values.append(int(level_val))
        for bid in self.bids:
            orderBook.cancel_order(bid)
        for ask in self.asks:
            orderBook.cancel_order(ask)
        self.bids, self.asks = [], []
        now = time_ns()
        if self.inventory < self.max_pos:
            for i, val in enumerate(adj_values):
                order = Order(now + i, self.firm_id, val - (self.spread_ticks // 2) - (i * 2), qty, "BUY", now)
                self.bids.append(order)

        if self.inventory > -self.max_pos:
            for i, val in enumerate(adj_values):
                order = Order(now + 100 + i, self.firm_id, val + (self.spread_ticks // 2) + (i * 2), qty, "SELL", now)
                self.asks.append(order)
        return self.bids, self.asks

    #if an order is filled, alter the inventory and the profit accordingly. else, refresh the quotes
    def on_event(self, orderBook, event_type:EventType, qty=None, side=None, initiator_id=None, price=None):
        if event_type == "FILL":
            assert qty != None and side != None
            self.inventory += (qty if side == "BUY" else -qty)
            self.cash -= (qty if side == "BUY" else -qty) * price
            self.pnl = self.inventory * price + self.cash
            self.last_prices.append(price)
            return
        if initiator_id == self.firm_id:
            return
        
        self.enter_spread(orderBook, initiator_id=self.firm_id)

    def enter_spread(self, orderBook, initiator_id=None):
        bids, asks = self.generate_spread(orderBook)
        for bid in bids:
            orderBook.process_order(bid, initiator_id=self.firm_id)
        for ask in asks: 
            orderBook.process_order(ask, initiator_id=self.firm_id)

    
    