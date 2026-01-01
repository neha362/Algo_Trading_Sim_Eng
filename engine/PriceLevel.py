import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from util.Deque import Deque, DequeNode
from engine.Order import Order
'''
- Price Level class
    - order objects at the same price
'''

class PriceLevel: 
    #initializer function that creates a price level of a certain price with an empty deque of orders and a total volume of 0
    def __init__(self, price):
        self.price = price
        self.orders:Deque[Order] = Deque()
        self.total_volume = 0
    
    #adds an order to the deque of orders by appending it to the end and changing the quantity
    def add_order(self, order:Order):
        self.orders.push(order)
        self.total_volume += order.quantity
        return self.orders.tail
    
    def remove_order(self, order:DequeNode[Order]):
        self.orders.remove(order)
        self.total_volume -= order.value.quantity
    
    def __str__(self):
        return f"price: ${self.price/100:.2f}, num orders: {len(self.orders)}, total volume: {self.total_volume}"