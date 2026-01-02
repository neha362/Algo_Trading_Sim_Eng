from datetime import date
from typing import *
from time import *
'''
- Order class
    - id, price, quantity, side, timestamp
    - store linked list position
'''

#literals to keep track of side
type Side = Literal["BUY", "SELL"]


class Order: 
    #initializer function for Orders that keeps track of id, price, quantity, side, timestamp, and queue position
    def __init__(self, id:int|None, firm_id, price:int, quantity:int, side:Side, timestamp:time):
        self.id = id
        self.firm_id = firm_id
        self.price = price
        self.quantity = quantity
        self.side = side
        self.timestamp = timestamp
        self.queuePos = -1
        
    
    #print function to visualize order
    def __str__(self):
        return f"id: {self.id}, firm id: {self.firm_id}, price: ${"None" if self.price == None else self.price/100:.2f}, qty: {self.quantity}, side:{self.side}, time:{ctime(self.timestamp/(10 ** 9))}:{self.timestamp % (10 ** 9):09}, pos:{self.queuePos}"