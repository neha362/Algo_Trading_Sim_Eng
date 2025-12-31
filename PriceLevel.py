from collections import deque
'''
- Price Level class
    - order objects at the same price
'''

class PriceLevel: 
    #initializer function that creates a price level of a certain price with an empty deque of orders and a total volume of 0
    def __init__(self, price):
        self.price = price
        self.orders = deque()
        self.total_volume = 0
    
    #adds an order to the deque of orders by appending it to the end and changing the quantity
    def add_order(self, order:Order):
        self.orders.append(order)
        self.total_volume += order.quantity
        print(f"added order {order} to {list(self.orders)}")
    
    def __str__(self):
        return f"price: {self.price}, num orders: {len(self.orders)}, total volume: {self.total_volume}"