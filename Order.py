from datetime import date
from typing import *
'''
- Order class
    - id, price, quantity, side, timestamp
    - store linked list position
'''

#literals to keep track of side
type Side = Literal["BUY", "SELL"]


class Order: 
    #initializer function for Orders that keeps track of id, price, quantity, side, timestamp, and queue position
    def __init__(self, id:int, price:int, quantity:int, side:Side, timestamp:date):
        self.id = id
        self.price = price
        self.quantity = quantity
        self.side = side
        self.timestamp = timestamp
        self.queuePos = -1
    
    #print function to visualize order
    def __str__(self):
        return f"id: {self.id}, price: {self.price}, qty: {self.quantity}, side:{self.side}, time:{self.timestamp.day}:{self.timestamp.hour}:{self.timestamp.minute}:{self.timestamp.second}, pos:{self.queuePos}"