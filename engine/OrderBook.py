from sortedcollections import SortedDict
from engine.Order import *
from engine.PriceLevel import *
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
    #inititalizes empty bid and ask dictionaries and an ordermap to access orders in O(1) time
    def __init__(self):
        self.bids = SortedDict()
        self.asks = SortedDict()
        self.ordermap = {}

    #cancels the order and removes it from its respective price level
    def cancel_order(self, order:Order):
        assert order.id in self.ordermap
        price_level = self.bids[-1 * order.price] if order.side == "BUY" else self.asks[order.price]
        price_level.remove(self.ordermap[order.id])
        del self.ordermap[order.id]
    
    #initiates the order process (i.e. checks if the order can be matched and if not then adds it to the opposing side)
    def process_order(self, order:Order):
        order = self.match_order(order)
        if order.quantity > 0:
            side = self.asks if order.side == "SELL" else self.bids
            price = order.price * (1 if order.side == "SELL" else -1)
            if price not in side:
                side[price] = PriceLevel(order.price)
            self.ordermap[order.id] = side[price].add_order(order)
    
    #matches the order (i.e. executes an order while a compatible order on the opposing side exists)
    def match_order(self, order:Order): 
        remove = []
        opp_side = self.bids if order.side == "SELL" else self.asks
        for price in opp_side:
            orig_price = price * (-1 if order.side == "SELL" else 1)
            if order.quantity <= 0:
                break
            if order.side == "SELL" and order.price > orig_price or order.side == "BUY" and order.price < orig_price:
                break
            self.execute_order(order, opp_side[price])
            if opp_side[price].total_volume == 0:
                remove.append(price)
                continue
        for price in remove:
            del opp_side[price]
        return order

    #executes the order (i.e. executes the minimum quantity at a satisfactory price)  
    def execute_order(self, order:Order, price_level:PriceLevel):
        while len(price_level.orders) > 0 and order.quantity > 0:
            if price_level.orders.peek().quantity == 0:
                price_level.orders.pop()
                continue
            curr_order = price_level.orders.peek()
            qty = min(curr_order.quantity, order.quantity)
            curr_order.quantity -= qty
            price_level.total_volume -= qty
            if curr_order.quantity <= 0:
                price_level.orders.pop()
                del self.ordermap[curr_order.id]
            order.quantity -= qty
            
    #helper function to print the order book
    def __str__(self):
        return f"ASKS:\n{self.asks}\nBIDS:\n{self.bids}"