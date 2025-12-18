from datetime import date
'''
- Order class
    - id, price, quantity, side, timestamp
    - store linked list position
'''

class Order: 
    def __init__(self, id:int, price:int, quantity:int, side:int, timestamp:date, queuePos:int):
        self.id = id
        self.price = price
        self.quantity = quantity
        self.side = side
        self.timestamp = timestamp
        self.queuePos = queuePos
    