from sortedcollections import ItemSortedDict
from Order import *
'''
- Order Book class
    - Keeps track of list of Bids and Asks
    - Implements price-time priority
        - higher bids and lower asks first
        - secondary time sorting

- matching algorithm 
    - price >= lowest ask
        - execute from front
    - else add to end
'''


class OrderBook: 
    def __init__(self):
        self.bids = ItemSortedDict(lambda _, value: -1 * value.price, [])
        self.asks = ItemSortedDict(lambda _, value: value.price, [])
        self.ordermap = {}
    
    def add_order(self, x:Order):
        (self.asks if x.side == "SELL" else self.bids)[x.id] = x
        self.ordermap[x.id] = x
        
    def print_book(self):
        print("ASKS")
        for i in self.asks:
            print(f"{i}:{self.asks[i]}")
        print("BIDS")
        for i in self.bids:
            print(f"{i}:{self.bids[i]}")