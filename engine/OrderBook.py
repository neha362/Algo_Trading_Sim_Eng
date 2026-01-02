from sortedcollections import SortedDict
from engine.Order import Order
from engine.PriceLevel import PriceLevel
from engine.MarketMaker import MarketMaker
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
        self.dollars_traded = 0
        self.shares_traded = 0
        self.mm_map = {}

    def register_mm(self, firm_id, market_maker:MarketMaker):
        if firm_id in self.mm_map:
            raise KeyError()
        self.mm_map[firm_id] = market_maker.on_fill

    #cancels the order and removes it from its respective price level
    def cancel_order(self, order:Order):
        assert order.id in self.ordermap
        price_level = self.bids[-1 * order.price] if order.side == "BUY" else self.asks[order.price]
        price_level.remove(self.ordermap[order.id])
        del self.ordermap[order.id]
    
    #initiates the order process (i.e. checks if the order can be matched and if not then adds it to the opposing side)
    def process_order(self, order:Order):
        order = self.match_order(order)
        if order.quantity > 0 and order.price != None:
            side = self.asks if order.side == "SELL" else self.bids
            price = order.price * (1 if order.side == "SELL" else -1)
            if price not in side:
                side[price] = PriceLevel(order.price)
            self.ordermap[order.id] = side[price].add_order(order)
        elif order.price == None and order.quantity > 0:
            print(f"cancelling market order with remaining quantity {order.quantity} on side {order.side}")
            return
            
    
    #matches the order (i.e. executes an order while a compatible order on the opposing side exists)
    def match_order(self, order:Order): 
        remove = []
        opp_side = self.bids if order.side == "SELL" else self.asks
        for price in opp_side:
            if order.quantity <= 0:
                break
            if order.price == None:
                self.execute_order(order, opp_side[price])
            else:
                orig_price = price * (-1 if order.side == "SELL" else 1)
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
            if order.firm_id == curr_order.firm_id:
                print(f"STP Triggered: Order {order.id} rejected to avoid wash trade with {curr_order.id}")
                order.quantity = 0
                return
            qty = min(curr_order.quantity, order.quantity)
            curr_order.quantity -= qty
            price_level.total_volume -= qty
            self.shares_traded += qty
            self.dollars_traded += qty * curr_order.price
            if curr_order.quantity <= 0:
                price_level.orders.pop()
                del self.ordermap[curr_order.id]
            order.quantity -= qty
            if curr_order.firm_id in self.mm_map:
                self.mm_map[curr_order.firm_id](qty, curr_order.side)
            if order.firm_id in self.mm_map:
                self.mm_map[order.firm_id](qty, order.side)
            
    #helper function to print the order book
    def __str__(self):
        return f"ASKS:\n{self.asks}\nBIDS:\n{self.bids}"