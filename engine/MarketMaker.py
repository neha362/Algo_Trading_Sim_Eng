from .Order import Order
from .OrderBook import OrderBook
from time import time_ns

#a market maker class to generate a bid and ask order based on current market orders to generate profit
class MarketMaker:
    #initializer with firm id, order book, and spread_ticks 
    def __init__(self, firm_id, orderBook:OrderBook, spread_ticks=10):
        self.orderBook = orderBook
        self.inventory = 0
        self.firm_id = firm_id
        self.spread_ticks = spread_ticks
        self.bid = None
        self.ask = None
        self.profit = 0
    
    #generates a spread and returns a bid and ask based on the best possible bid and ask
    def generate_spread(self, qty=10):
        best_bid = self.orderBook.bids.peekitem()[0] if self.orderBook.bids else None
        best_ask = self.orderBook.asks.peekitem()[0] if self.orderBook.asks else None
        adj_value = 100 if not best_bid or not best_ask else (best_bid + best_ask)//2 - self.inventory * 2
        if self.bid != None:
            self.orderBook.cancel_order(self.bid)
        if self.ask != None:
            self.orderBook.cancel_order(self.ask)
        self.bid = Order(time_ns(), self.firm_id, adj_value - self.spread_ticks // 2, qty, "BUY", time_ns())
        self.ask = Order(time_ns() + 1, self.firm_id, adj_value + self.spread_ticks // 2, qty, "SELL", time_ns())
        return self.bid, self.ask

    #if an order is filled, alter the inventory and the profit accordingly
    def on_fill(self, qty, side):
        self.inventory += qty * (1 if side == "BUY" else -1)
        self.profit += qty * (self.bid.price if side == "BUY" else -self.ask.price)
        bid, ask = self.generate_spread()
        self.orderBook.process_order(bid)
        self.orderBook.process_order(ask)